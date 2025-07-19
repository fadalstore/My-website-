from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, URLField
from wtforms.validators import DataRequired, Email, Length, URL

class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    content = TextAreaField('Comment', validators=[DataRequired(), Length(max=1000)])

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=2000)])

class LinkSubmissionForm(FlaskForm):
    title_en = StringField('Title (English)', validators=[DataRequired(), Length(max=200)])
    title_so = StringField('Title (Somali)', validators=[Length(max=200)])
    description_en = TextAreaField('Description (English)', validators=[Length(max=500)])
    description_so = TextAreaField('Description (Somali)', validators=[Length(max=500)])
    url = URLField('URL', validators=[DataRequired(), URL(), Length(max=500)])
    category_id = SelectField('Category', coerce=int)
    submitted_by = StringField('Your Name', validators=[DataRequired(), Length(max=100)])
    submitter_email = StringField('Your Email', validators=[DataRequired(), Email(), Length(max=120)])
    
    def __init__(self, *args, **kwargs):
        super(LinkSubmissionForm, self).__init__(*args, **kwargs)
        from models import Category
        self.category_id.choices = [(c.id, c.name_en) for c in Category.query.all()]
