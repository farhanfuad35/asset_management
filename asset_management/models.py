from django.db import models
from datetime import datetime
from user_management.models import Company, Employee


class AssetTypes(models.Model):
    """
    Defines asset types ie. Phone, Laptop etc.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100, default="")


class Asset(models.Model):
    """
    Keeps the record of all the assets. Each asset gets a row in this table.
    """

    def get_unknown_type():
        return AssetTypes.objects.get_or_create(name="Unknown")[0]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="company_assets",
        help_text="Company the asset belongs to",
    )

    # Company given asset id
    asset_id = models.CharField(max_length=100)

    asset_type = models.ForeignKey(
        AssetTypes, related_name="items", on_delete=models.SET(get_unknown_type)
    )
    manufacturer = models.CharField(max_length=100)
    purchased_at = models.DateTimeField()
    purchased_from = models.CharField(max_length=100)

    # Based on the assumption that one asset can be owned by at most a single user at any moment
    current_owner = models.ForeignKey(
        Employee, on_delete=models.RESTRICT, null=True, related_name="my_assets"
    )

    def get_last_log(self):
        return Log.objects.filter(asset=self)[0]

    def in_company_stock(self):
        log = self.get_last_log()
        if log is None:
            return True
        if log.recieved_at is None:
            return False
        else:
            return True

    def assign_to(self, user: Employee):
        if self.in_company_stock():
            self.current_owner = user
            self.save()
            log = Log(asset=self, owner=user)
            log.save()
        else:
            raise AssetNotInStock(self.asset_id, self.current_owner)

    def returned_to_company(self):
        log = self.get_last_log()
        if log is not None:
            log.recieved_at = datetime.now()
            log.save()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["asset_id", "company"], name="unique_asset_per_company"
            )
        ]

    class AssetNotInStock(Exception):
        def __init__(self, asset_id: int, current_owner: Employee):
            message = f"The asset {asset_id} currently is not in company stock. Current owner of the asset is {current_owner.name}"
            super().__init__()


class Log(models.Model):
    """
    Keeps the log of each borrow/return event. Variables are named from the admin's/company's perspective
    """

    def get_current_owner(self):
        return self.asset.current_owner

    def get_sentinel_user(self):
        return Employee.objects.get_or_create()

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="logs")
    owner = models.ForeignKey(Employee, on_delete=models.SET(get_sentinel_user))
    distributed_at = models.DateTimeField(auto_now_add=True)
    recieved_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ["-distributed_at"]
