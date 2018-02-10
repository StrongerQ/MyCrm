from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    '''客户信息表'''
    name = models.CharField(max_length=32,blank=True,null=True) #blank是ADMIN空,null是数据库
    qq = models.CharField(max_length=64,unique=True)
    qq_name = models.CharField(max_length=64,blank=True,null=True)
    Phone = models.CharField(max_length=32,blank=True,null=True)
    source_chioces = (
        (0, '转介绍'),
        (1, 'QQ群'),
        (2, '官网'),
        (3, '百度推广'),
        (4, '51CTO'),
        (5, '知乎'),
        (6, '市场推广'),
    )
    source = models.SmallIntegerField(choices=source_chioces)
    referral_from = models.CharField(verbose_name='介绍人',max_length=64,blank=True,null=True)
    consult_course = models.ForeignKey('Course',verbose_name='咨询课程',on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag',blank=True,null=True,verbose_name='标签')
    content = models.TextField(verbose_name='咨询详情')
    contsultant = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    note = models.TextField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.qq
    class Meta:
        verbose_name_plural = '客户信息表'

class Tag(models.Model):
    '''标签'''
    name =models.CharField(unique=True,max_length=32)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '标签'

class CustomerFollowUp(models.Model):
    '''客户记录表'''
    customer = models.ForeignKey('Customer',on_delete=models.CASCADE)
    content = models.TextField(verbose_name='跟进内容')
    contsultant = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    intention_choices = (
        (0,'2周内报名'),
        (1,'1个月内报名'),
        (2,'近期无报名计划'),
        (3,'已在其他机构报名'),
        (4,'已报名'),
        (5,'已拉黑'),
    )
    intention = models.SmallIntegerField(choices=intention_choices)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<%s:%s>' %(self.customer.qq,self.intention)
    class Meta:
        verbose_name_plural = '客户记录表'

class Course(models.Model):
    '''课程表'''
    name = models.CharField(max_length=64,unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name='学习周期(月)')
    outline = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '课程表'

class Branch(models.Model):
    '''校区'''
    name = models.CharField(max_length=128,unique=True)
    addr = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '校区'

class ClassList(models.Model):
    '''班级表'''
    course = models.ForeignKey('Course',on_delete=models.CASCADE)
    semerter = models.PositiveSmallIntegerField(verbose_name='学期')
    teachers = models.ManyToManyField('UserProfile')
    branch = models.ForeignKey('Branch',verbose_name='校区',on_delete=models.CASCADE)
    class_type_choices = (
        (0,'周末面授'),
        (1,'脱产面授'),
        (2,'网络'),
    )
    class_type = models.SmallIntegerField(choices=class_type_choices,verbose_name='班级类型')
    start_date = models.DateField(verbose_name='开班日期')
    end_date = models.DateField(verbose_name='结业日期',blank=True,null=True)

    def __str__(self):
        return '<%s,%s,%s>'%(self.branch,self.course,self.semerter)
    class Meta:
        unique_together = ('branch','course','semerter')
        verbose_name_plural = '班级'

class CourseRecord(models.Model):
    '''上课记录表'''
    from_class = models.ForeignKey('ClassList',verbose_name='班级',on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField(verbose_name='第几天')
    teacher = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    has_homework = models.BooleanField(default=True)
    homework_title = models.CharField(max_length=128,blank=True,null=True)
    homework_content = models.TextField(blank=True,null=True)
    outline = models.TextField(verbose_name='课程大纲')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s %s' %(self.from_class,self.day_num)
    class  Meta:
        unique_together = ('from_class','day_num')
        verbose_name_plural = '上课记录表'

class StudyRecord(models.Model):
    '''学习记录表'''
    student = models.ForeignKey('Enrollment',on_delete=models.CASCADE)
    course_record = models.ForeignKey('CourseRecord',on_delete=models.CASCADE)
    attendance_choices = (
        (0,'签到'),
        (1,'迟到'),
        (2,'缺勤'),
        (3,'早退'),
    )
    attendance = models.SmallIntegerField(choices=attendance_choices,default=0)
    score_choices = (
        (100,'A+'),
        (90,'A'),
        (85,'B+'),
        (80,'B'),
        (75,'B-'),
        (70,'C+'),
        (60,'C'),
        (40,'C-'),
        (0,'N/A'),
        (-50,'D'),
        (-100,'COPY'),
    )
    score = models.PositiveSmallIntegerField(choices=score_choices)
    memo = models.TextField(blank=True,null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s %s %s'%(self.student,self.course_record,self.score)
    class Meta:
        unique_together = ('student','course_record')
        verbose_name_plural = '学习记录表'

class Enrollment(models.Model):
    '''报名表'''
    customer = models.ForeignKey('Customer',on_delete=models.CASCADE)
    enrolled_class = models.ForeignKey('ClassList',verbose_name='报名班级',on_delete=models.CASCADE)
    consultant = models.ForeignKey('UserProfile',verbose_name='课程顾问',on_delete=models.CASCADE)
    contract_aggreed = models.BooleanField(default=False,verbose_name='学员同意合同条款')
    contract_approval = models.BooleanField(default=False,verbose_name='审核合同')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' %(self.customer,self.enrolled_class)

    class Meta:
        unique_together = ('customer','enrolled_class')
        verbose_name_plural = '报名表'

class Payment(models.Model):
    '''缴费记录'''
    customer = models.ForeignKey('Customer',on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name='数额',default=500)
    course = models.ForeignKey('Course',verbose_name='报名课程',on_delete=models.CASCADE)
    consultant = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' %(self.customer,self.amount)
    class Meta:
        verbose_name_plural = '缴费记录'

class UserProfile(models.Model):
    '''账户表'''
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    roles = models.ManyToManyField('Role',blank=True,null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '账户表'

class Role(models.Model):
    '''角色表'''
    name = models.CharField(max_length=32,unique=True)
    meuns = models.ManyToManyField('Menu',blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '角色表'

class Menu(models.Model):
    '''菜单'''
    name = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64)

    def __str__(self):
        return  self.name
    class Meta:
        verbose_name_plural = '菜单'