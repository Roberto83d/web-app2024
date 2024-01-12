from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class PurchaseForm(FlaskForm):
    product_name = StringField('Nazwa produktu', validators=[DataRequired()], render_kw={"placeholder": "Wpisz nazwę produktu"})
    unit_price = DecimalField('Cena jednostkowa', validators=[DataRequired()], places=2, render_kw={"placeholder": "Wpisz cenę jednostkową"})
    quantity = IntegerField('Liczba sztuk', validators=[DataRequired()], render_kw={"placeholder": "Wpisz liczbę sztuk"})
    submit = SubmitField('Zakup')

class SaleForm(FlaskForm):
    product_name = StringField('Nazwa produktu', validators=[DataRequired()], render_kw={"placeholder": "Wpisz nazwę produktu"})
    unit_price = DecimalField('Cena jednostkowa', validators=[DataRequired()], places=2, render_kw={"placeholder": "Wpisz cenę jednostkową"})
    quantity = IntegerField('Liczba sztuk', validators=[DataRequired()], render_kw={"placeholder": "Wpisz liczbę sztuk"})
    submit = SubmitField('Sprzedaż')

class BalanceForm(FlaskForm):
    comment = StringField('Komentarz', validators=[DataRequired()], render_kw={"placeholder": "Wpisz komentarz"})
    value = DecimalField('Wartość', validators=[DataRequired()], places=2, render_kw={"placeholder": "Wpisz wartość"})
    submit = SubmitField('Zmień saldo')
