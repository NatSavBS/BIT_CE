from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from CEForm.auth import login_required
from CEForm.db import get_db

bp = Blueprint("secure", __name__, url_prefix='/secure')

@login_required
@bp.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("secure/form.html")
    if request.method == "POST":
        error = ""
        #check all fields are valid
        for X in ["CompanyName", "BusinessArea", "Line1", "Line2", "City", "Country", "Postcode", "ContactName", "ContactEmail", "ContactPhone"]:
            if request.form.get(X, '').strip() == '':
                error += f"{X} cannot be blank"
        if error:
            flash(error)
            return render_template("secure/form.html")

        else:
            print(request.form)
            return redirect("secure.submitted")

@login_required
@bp.route('/submitted')
def submitted():
    return render_template("secure/submitted.html")




