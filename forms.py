from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp, Email

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField, FloatField, \
    Form, FormField, FieldList, IntegerField
from wtforms.validators import DataRequired, InputRequired, NumberRange


# Set your classes here.


class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

min_assetNum        = 1
max_assetNum        = 10
min_owner_pct       = 0.01
max_owner_pct       = 0.5
min_entryVal        = 10
max_entryVal        = 1000
min_periodYears     = 5
max_periodYears     = 15
min_growthRate      = 0.00
max_growthRate      = 1.5
min_samples         = 100
max_samples         = 100000
msg_required_field  = "This is a required field!"
msg_range           = "Value should be between {} - {}. "
min_growthRate      = 1.0
max_growthRate      = 10.0

# exponential
# normal
# lognormal
# randomunif

dist = ['exponential','normal','lognormal','randomunif']
name_dist = ['Exponential','Normal-Gaussian','Log-Normal','Random-Uniform']
option_samples = [100,1000,5000,10000,50000,100000]
text_option_samples  = ['100','1,000','5,000','10,000','50,000','100,000']

class LoginForm(FlaskForm):
    email       = StringField("Email", validators=[InputRequired(msg_required_field)])
    password    = StringField("Password", validators=[InputRequired(msg_required_field)])
    remember_me = BooleanField("Remember Me")
    submit      = SubmitField("Login")

class RegisterForm(FlaskForm):
    email               = StringField("Email", validators=[InputRequired(msg_required_field)])
    password            = StringField("Password", validators=[InputRequired(msg_required_field)])
    password_confirm    = StringField("confirm Password", validators=[InputRequired(msg_required_field)])
    first_name          = StringField("First Name", validators=[InputRequired(msg_required_field)])
    last_name           = StringField("Password", validators=[InputRequired(msg_required_field)])
    submit              = SubmitField("Register now")




class AssetBaseForm(FlaskForm):

    assetName = StringField("Asset Name",default= "Asset 1", validators=[InputRequired(msg_required_field)])
    entryVal = FloatField("Entry Valuation",default= 100, validators=[InputRequired(msg_required_field),
                                                          NumberRange(min=min_entryVal,
                                                                      max=max_entryVal,
                                                                      message=msg_range.format(max_entryVal,max_entryVal))])

    ownPercent = FloatField("Ownership Percentage", default=0.2, validators=[InputRequired(msg_required_field),
                                                                 NumberRange(min=min_owner_pct,
                                                                             max=max_owner_pct,
                                                                             message=msg_range.format(min_owner_pct,
                                                                                                      max_owner_pct))])
    periodYears = IntegerField("Time Period", default= 10, validators=[InputRequired(msg_required_field),
                                                                 NumberRange(min=min_periodYears,
                                                                             max=max_periodYears,
                                                                             message=msg_range.format(min_periodYears,
                                                                                                      max_periodYears))])

    growthRate = FloatField("Expected Annual Growth Rate", default=1.25 ,validators=[InputRequired(msg_required_field),
                                                                 NumberRange(min=min_growthRate,
                                                                             max=max_growthRate,
                                                                             message=msg_range.format(min_growthRate,
                                                                                                      max_growthRate))])
    sigma = FloatField("Standard Deviation", validators=[])
#     These two fields are done at portfolio level
#    dist = StringField("Distribution", validators=[InputRequired(msg_required_field)])
#     samples = StringField("Number of Samples", validators=[InputRequired(msg_required_field),
#                                                                  NumberRange(min=min_samples,
#                                                                              max=max_samples,
#                                                                              message=msg_range.format(min_samples,
#
#                                                                                                       max_samples))])
# #======================================================================================

class AssetForm(AssetBaseForm):
    dist = SelectField("Distribution", choices=list(zip(dist, name_dist)),
                       validators=[InputRequired(msg_required_field)])
    # dist = StringField("Distribution", validators=[InputRequired(msg_required_field)])
    samples = StringField("Number of Samples", validators=[InputRequired(msg_required_field),
                                                                     NumberRange(min=min_samples,
                                                                                 max=max_samples,
                                                                                 message=msg_range.format(min_samples,

                                                                                                          max_samples))])





class PortfolioForm(FlaskForm):
    portfolioName = StringField("Asset Name", validators=[InputRequired(msg_required_field)])
    # dist = StringField("Distribution", validators=[InputRequired(msg_required_field)])
    dist = SelectField("Distribution",choices=list(zip(dist,name_dist)) ,
                       validators=[InputRequired(msg_required_field)])

    num_samples = SelectField("Samples", choices=list(zip(option_samples, text_option_samples)),
                       validators=[InputRequired(msg_required_field)])
    num_assets = IntegerField("Number of Asset in Portfolio",validators=[InputRequired(msg_required_field),
                                                                 NumberRange(min=min_growthRate,
                                                                             max=max_growthRate,
                                                                             message=msg_range.format(min_growthRate,
                                                                                                      max_growthRate))])

class PortfolioAssetForm(PortfolioForm):
    assetContent = FieldList(FormField(AssetBaseForm), min_entries=1)


class CompareAssetForm(FlaskForm):
    a_assetName = StringField("Asset Name", default="Asset 1", validators=[InputRequired(msg_required_field)])
    a_entryVal = FloatField("Entry Valuation", default=100, validators=[InputRequired(msg_required_field),
                                                                      NumberRange(min=min_entryVal,
                                                                                  max=max_entryVal,
                                                                                  message=msg_range.format(max_entryVal,
                                                                                                           max_entryVal))])

    a_ownPercent = FloatField("Ownership Percentage", default=0.2, validators=[InputRequired(msg_required_field),
                                                                               NumberRange(min=min_owner_pct,
                                                                                           max=max_owner_pct,
                                                                                           message=msg_range.format(
                                                                                               min_owner_pct,
                                                                                               max_owner_pct))])
    a_periodYears = IntegerField("Time Period", default=10, validators=[InputRequired(msg_required_field),
                                                                      NumberRange(min=min_periodYears,
                                                                                  max=max_periodYears,
                                                                                  message=msg_range.format(
                                                                                      min_periodYears,
                                                                                      max_periodYears))])

    a_growthRate = FloatField("Expected Annual Growth Rate", default=1.25, validators=[InputRequired(msg_required_field),
                                                                                     NumberRange(min=min_growthRate,
                                                                                                 max=max_growthRate,
                                                                                                 message=msg_range.format(
                                                                                                     min_growthRate,
                                                                                                     max_growthRate))])
    a_sigma = FloatField("Standard Deviation", validators=[])

    a_dist = SelectField("Distribution", choices=list(zip(dist, name_dist)),
                       validators=[InputRequired(msg_required_field)])
    # dist = StringField("Distribution", validators=[InputRequired(msg_required_field)])

    b_assetName = StringField("Asset Name", default="Asset 2", validators=[InputRequired(msg_required_field)])
    b_entryVal = FloatField("Entry Valuation", default=100, validators=[InputRequired(msg_required_field),
                                                                        NumberRange(min=min_entryVal,
                                                                                    max=max_entryVal,
                                                                                    message=msg_range.format(
                                                                                        max_entryVal,
                                                                                        max_entryVal))])

    b_ownPercent = FloatField("Ownership Percentage", default=0.2, validators=[InputRequired(msg_required_field),
                                                                                 NumberRange(min=min_owner_pct,
                                                                                             max=max_owner_pct,
                                                                                             message=msg_range.format(
                                                                                                 min_owner_pct,
                                                                                                 max_owner_pct))])
    b_periodYears = IntegerField("Time Period", default=10, validators=[InputRequired(msg_required_field),
                                                                        NumberRange(min=min_periodYears,
                                                                                    max=max_periodYears,
                                                                                    message=msg_range.format(
                                                                                        min_periodYears,
                                                                                        max_periodYears))])

    b_growthRate = FloatField("Expected Annual Growth Rate", default=1.25,
                              validators=[InputRequired(msg_required_field),
                                          NumberRange(min=min_growthRate,
                                                      max=max_growthRate,
                                                      message=msg_range.format(
                                                          min_growthRate,
                                                          max_growthRate))])
    b_sigma = FloatField("Standard Deviation", validators=[])

    b_dist = SelectField("Distribution", choices=list(zip(dist, name_dist)),
                         validators=[InputRequired(msg_required_field)])
    # dist = StringField("Distribution", validators=[InputRequired(msg_required_field)])


    samples = SelectField("Samples", choices=list(zip(option_samples, text_option_samples)),
                       validators=[InputRequired(msg_required_field)])




class PramsTxMatrixInputForm(FlaskForm):

    initial_population = FloatField("Initial Investment", default=100000000, validators=[InputRequired(msg_required_field)
        , NumberRange(min=10000000, max=10000000000, message=msg_range.format(100000000, 10000000000))])

    round_seed_a = FloatField("Seed-RoundA", default=0.2, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_seed_failure = FloatField("Seed-Failure", default=0.2, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_a_b = FloatField("RoundA-RoundB", default=0.2, validators=[InputRequired(msg_required_field)
        ,NumberRange(min=0, max=1, message=msg_range.format(0,1))])

    round_a_failure = FloatField("RoundA-Failure", default=0.2, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_b_c = FloatField("RoundB-RoundC", default=0.2, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_b_failure = FloatField("RoundB-Failure", default=0.2, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_c_success = FloatField("RoundC-Success", default=0.2, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_c_failure = FloatField("RoundC-Failure", default=0.2, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_success_success = FloatField("Success-Success", default=0.2, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_success_failure = FloatField("Success-Failure", default=0.2, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_failure_success = FloatField("Failure-Success", default=0.2, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_failure_failure = FloatField("Failure-Failure", default=0.2, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    # initial_population
    # round_seed_a
    # round_seed_failure
    # round_a_b
    # round_a_failure
    # round_b_c
    # round_b_failure
    # round_c_success
    # round_c_failure
    # round_success_success
    # round_success_failure
    # round_failure_success
    # round_failure_failure


class AddressEntryForm(FlaskForm):
    name = StringField("Asset Name", default="Asset 1", validators=[InputRequired(msg_required_field)])

class AddressesForm(FlaskForm):
    """A form for one or more addresses"""
    addresses = FieldList(FormField(AddressEntryForm), min_entries=1)
    data = FieldList(FormField(PramsTxMatrixInputForm), min_entries=1)


class PramsTxMatrixInputFormLarge(FlaskForm):

    initial_population = FloatField("Initial Investment", default=1000, validators=[InputRequired(msg_required_field)
        , NumberRange(min=1000, max=10000000000, message=msg_range.format(100000000, 10000000000))])

    round_seed_a = FloatField("Seed-RoundA", default=0.3, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_seed_failure = FloatField("Seed-Failure", default=0.67, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_a_b = FloatField("RoundA-RoundB", default=0.2, validators=[InputRequired(msg_required_field)
        ,NumberRange(min=0, max=1, message=msg_range.format(0,1))])

    round_a_failure = FloatField("RoundA-Failure", default=0.3, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_b_c = FloatField("RoundB-RoundC", default=0.3, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_b_failure = FloatField("RoundB-Failure", default=0.2, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_c_success = FloatField("RoundC-Success", default=0.3, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_c_failure = FloatField("RoundC-Failure", default=0.4, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_success_success = FloatField("Success-Success", default=1, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_success_failure = FloatField("Success-Failure", default=0, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_failure_success = FloatField("Failure-Success", default=0, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_failure_failure = FloatField("Failure-Failure", default=1, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_a_a = FloatField("RoundA-RoundA", default=0.4, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_b_b= FloatField("RoundB-RoundB", default=0.3, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    round_c_c= FloatField("RoundC-RoundC", default=0.3, validators=[InputRequired(msg_required_field)
        , NumberRange(min=0, max=1, message=msg_range.format(0, 1))])

    growth_a = FloatField("Growth Rate at Stage A", default=1.8, validators=[InputRequired(msg_required_field)
        , NumberRange(min=1, max=10, message=msg_range.format(1, 10))])

    growth_b = FloatField("Growth Rate at Stage B", default=2.2, validators=[InputRequired(msg_required_field)
        , NumberRange(min=1, max=10, message=msg_range.format(1, 10))])

    growth_c = FloatField("Growth Rate at Stage C", default=2.7, validators=[InputRequired(msg_required_field)
        , NumberRange(min=1, max=10, message=msg_range.format(1, 10))])

    growth_success = FloatField("Growth Rate after Success", default=1.25, validators=[InputRequired(msg_required_field)
        , NumberRange(min=1, max=10, message=msg_range.format(1, 10))])

