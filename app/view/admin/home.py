from flask import Blueprint, request, render_template, redirect, url_for
from . import admin


@admin.route('/', methods=['GET', 'POST'])
def index():

    return url_for('admin.catch_data')
