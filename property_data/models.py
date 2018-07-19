from django.db import models


class EscrowBalance(models.Model):

    app_label = 'property_data'

    # REVIEW:  finish adding in indexes
    # REVIEW:  finish adding in blank=True, null=True

    master_account_num = models.BigIntegerField('Master account number')
    master_account_name = models.CharField('Master account name', max_length = 128)
    sub_account_num = models.BigIntegerField('Sub account number')
    sub_account_name = models.CharField('Sub account name', max_length = 128)
    short_name = models.CharField('Short name', max_length = 128)
    account_status = models.CharField('Account status', max_length = 8)
    group_num = models.BigIntegerField('Group num')
    item_num = models.BigIntegerField('Item num (reference num)', db_index=True)
    original_balance = models.DecimalField('Original balance', max_digits=8, decimal_places=2)
    fed_withholding_tax_this_period = models.DecimalField('Fed Withholding tax this period', max_digits=8, decimal_places=2, null=True)
    ytd_fed_withholding_tax = models.DecimalField('YTD Fed Withholding tax', max_digits=8, decimal_places=2, null=True)
    int_paid_this_period = models.DecimalField('Interest paid this period', max_digits=8, decimal_places=2, null=True)
    ytd_int_paid = models.DecimalField('YTD interest paid', max_digits=8, decimal_places=2, null=True)
    int_split_this_period = models.DecimalField('Interest split this period', max_digits=8, decimal_places=2, null=True)
    escrow_balance = models.DecimalField('Escrow balance', max_digits=8, decimal_places=2)

    def convert_decimal(self, decimal):

        return str(decimal) if decimal else None

    def to_json(self):
        """
        Return json version of this object.
        """

        return {
            "master_account_num": self.master_account_num,
            "master_account_name": self.master_account_name,
            "sub_account_num": self.sub_account_num,
            "sub_account_name": self.sub_account_name,
            "short_name": self.short_name,
            "account_status": self.account_status,
            "group_num": self.group_num,
            "item_num": self.item_num,
            "original_balance": self.convert_decimal(self.original_balance),
            "fed_withholding_tax_this_period": self.convert_decimal(self.fed_withholding_tax_this_period),
            "ytd_fed_withholding_tax": self.convert_decimal(self.ytd_fed_withholding_tax),
            "int_paid_this_period": self.convert_decimal(self.int_paid_this_period),
            "ytd_int_paid": self.convert_decimal(self.ytd_int_paid),
            "int_split_this_period": self.convert_decimal(self.int_split_this_period),
            "escrow_balance": self.convert_decimal(self.escrow_balance),
        }

    def __str__(self):  # pragma: no cover (mostly for debugging)

        return "item num " + str(self.item_num) + " - " + self.sub_account_name
