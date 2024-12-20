from django.db import models
_model_cache = {}

class Attendancetable(models.Model):
    recordid = models.AutoField(db_column='RecordID', primary_key=True)  # Field name made lowercase. The composite primary key (RecordID, EmployeeID, Date) found, that is not supported. The first column is selected.
    employeeid = models.ForeignKey('Employeetable', models.DO_NOTHING, db_column='EmployeeID')  # Field name made lowercase.
    date = models.ForeignKey('Workdaytable', models.DO_NOTHING, db_column='Date')  # Field name made lowercase.
    clockintime = models.TimeField(db_column='ClockInTime', blank=True, null=True)  # Field name made lowercase.
    clockouttime = models.TimeField(db_column='ClockOutTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'attendancetable'
        unique_together = (('recordid', 'employeeid', 'date'),)


class Bonustable(models.Model):
    bonusid = models.AutoField(db_column='BonusID', primary_key=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2)  # Field name made lowercase.
    paymentdate = models.DateField(db_column='PaymentDate')  # Field name made lowercase.
    reason = models.TextField(db_column='Reason', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bonustable'


class Employeebonustable(models.Model):
    employeeid = models.IntegerField(db_column='EmployeeID', primary_key=True)  # Field name made lowercase. The composite primary key (EmployeeID, BonusID) found, that is not supported. The first column is selected.
    bonusid = models.ForeignKey(Bonustable, models.DO_NOTHING, db_column='BonusID')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2)  # Field name made lowercase.
    paymentdate = models.DateField(db_column='PaymentDate')  # Field name made lowercase.
    reason = models.TextField(db_column='Reason', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employeebonustable'
        unique_together = (('employeeid', 'bonusid'),)


class Employeepositiontable(models.Model):
    employeeid = models.OneToOneField('Employeetable', models.DO_NOTHING, db_column='EmployeeID', primary_key=True)  # Field name made lowercase. The composite primary key (EmployeeID, PositionName) found, that is not supported. The first column is selected.
    positionname = models.ForeignKey('Positiontable', models.DO_NOTHING, db_column='PositionName')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employeepositiontable'
        unique_together = (('employeeid', 'positionname'),)


class Employeesocialsecurityandhousingfundtable(models.Model):
    employeeid = models.OneToOneField('Employeetable', models.DO_NOTHING, db_column='EmployeeID', primary_key=True)
    projectname = models.ForeignKey('Socialsecurityandhousingfundtable', models.DO_NOTHING, db_column='ProjectName')
    amountdue = models.DecimalField(db_column='AmountDue', max_digits=10, decimal_places=2, blank=True, null=True)
    paymentdate = models.ForeignKey('Workdaytable', models.DO_NOTHING, db_column='PaymentDate')
    contributionrate = models.ForeignKey('Socialsecurityandhousingfundtable', models.DO_NOTHING, db_column='ContributionRate', to_field='contributionrate', related_name='employeesocialsecurityandhousingfundtable_contributionrate_set')

    class Meta:
        managed = False
        db_table = 'employeesocialsecurityandhousingfundtable'
        unique_together = (('employeeid', 'projectname', 'paymentdate'),)


class Employeetable(models.Model):
    employeeid = models.AutoField(db_column='EmployeeID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=6)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employeetable'


class Employeetaxtable(models.Model):
    employeeid = models.OneToOneField(Employeetable, models.DO_NOTHING, db_column='EmployeeID', primary_key=True)  # Field name made lowercase. The composite primary key (EmployeeID, TaxName, PaymentDate) found, that is not supported. The first column is selected.
    taxname = models.ForeignKey('Taxtable', models.DO_NOTHING, db_column='TaxName')  # Field name made lowercase.
    taxamount = models.DecimalField(db_column='TaxAmount', max_digits=10, decimal_places=2)  # Field name made lowercase.
    paymentdate = models.ForeignKey('Workdaytable', models.DO_NOTHING, db_column='PaymentDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employeetaxtable'
        unique_together = (('employeeid', 'taxname', 'paymentdate'),)


class Grosssalary(models.Model):
    employeeid = models.OneToOneField(Employeetable, models.DO_NOTHING, db_column='EmployeeID', primary_key=True)
    year = models.IntegerField(db_column='Year')
    month = models.IntegerField(db_column='Month')
    basesalary = models.ForeignKey('Positiontable', models.DO_NOTHING, db_column='BaseSalary', to_field='basesalary', blank=True, null=True)
    absentdeduction = models.DecimalField(db_column='AbsentDeduction', max_digits=10, decimal_places=2, blank=True, null=True)
    overtimepay = models.DecimalField(db_column='OvertimePay', max_digits=10, decimal_places=2, blank=True, null=True)
    performancebonus = models.DecimalField(db_column='PerformanceBonus', max_digits=10, decimal_places=2, blank=True, null=True)
    yearendbonus = models.DecimalField(db_column='YearEndBonus', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grosssalary'
        unique_together = (('employeeid', 'year', 'month'),)


class Performanceevaluationtable(models.Model):
    employeeid = models.IntegerField(db_column='EmployeeID', primary_key=True)  # Field name made lowercase. The composite primary key (EmployeeID, IndicatorName, EvaluationDate) found, that is not supported. The first column is selected.
    indicatorname = models.ForeignKey('Performancetable', models.DO_NOTHING, db_column='IndicatorName')  # Field name made lowercase.
    score = models.DecimalField(db_column='Score', max_digits=5, decimal_places=2)  # Field name made lowercase.
    evaluationdate = models.DateField(db_column='EvaluationDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'performanceevaluationtable'
        unique_together = (('employeeid', 'indicatorname', 'evaluationdate'),)


class Performancetable(models.Model):
    indicatorname = models.CharField(db_column='IndicatorName', primary_key=True, max_length=100)  # Field name made lowercase.
    weight = models.DecimalField(db_column='Weight', max_digits=5, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'performancetable'


class Positiontable(models.Model):
    positionname = models.CharField(db_column='PositionName', primary_key=True, max_length=100)
    basesalary = models.DecimalField(db_column='BaseSalary', max_digits=10, decimal_places=2, unique=True)  # 设置为唯一

    class Meta:
        managed = False
        db_table = 'positiontable'


class Socialsecurityandhousingfundtable(models.Model):
    projectname = models.CharField(db_column='ProjectName', primary_key=True, max_length=100)
    contributionrate = models.DecimalField(db_column='ContributionRate', max_digits=5, decimal_places=2, unique=True)  # 设置为唯一

    class Meta:
        managed = False
        db_table = 'socialsecurityandhousingfundtable'


class Taxtable(models.Model):
    taxname = models.CharField(db_column='TaxName', primary_key=True, max_length=100)  # Field name made lowercase.
    lowerlimit = models.DecimalField(db_column='LowerLimit', max_digits=10, decimal_places=2)  # Field name made lowercase.
    upperlimit = models.DecimalField(db_column='UpperLimit', max_digits=10, decimal_places=2)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=5, decimal_places=2)  # Field name made lowercase.
    quickdeduction = models.DecimalField(db_column='QuickDeduction', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'taxtable'


class Workdaytable(models.Model):
    date = models.DateField(db_column='Date', primary_key=True)  # Field name made lowercase.
    isworkday = models.IntegerField(db_column='IsWorkday')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'workdaytable'

from django.db import models, connection
from django.utils.functional import cached_property

class DynamicSalaryView(models.Model):
    employeeid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    basesalary = models.DecimalField(max_digits=10, decimal_places=2)
    absentdeduction = models.DecimalField(max_digits=10, decimal_places=2)
    overtimepay = models.DecimalField(max_digits=10, decimal_places=2)
    performancebonus = models.DecimalField(max_digits=10, decimal_places=2)
    yearendbonus = models.DecimalField(max_digits=10, decimal_places=2)
    socialsecurityandhousingfund = models.DecimalField(max_digits=10, decimal_places=2)
    incometax = models.DecimalField(max_digits=10, decimal_places=2)
    netsalary = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True


def get_salary_view_model(year_month):
    # 替换连字符为下划线以匹配视图名称
    formatted_year_month = year_month.replace('-', '_')

    # 构建模型名称
    model_name = f'SalaryView{formatted_year_month}'

    # 如果模型已经存在于缓存中，则直接返回
    if model_name in _model_cache:
        return _model_cache[model_name]

    class Meta:
        db_table = f'SalaryView_{formatted_year_month}'
        managed = False

    attrs = {
        '__module__': DynamicSalaryView.__module__,  # 设置新类的模块属性
        'Meta': Meta,  # 将内部的 Meta 类添加到新类中
    }

    # 动态创建新的模型类并缓存它
    model_class = type(model_name, (DynamicSalaryView,), attrs)
    _model_cache[model_name] = model_class

    return model_class