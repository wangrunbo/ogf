from flask import Blueprint, request, render_template, redirect, url_for
from . import admin


@admin.route('/system', methods=['GET', 'POST'])
def system():
    return render_template('admin/system/index.html')


@admin.route('/system/catch_data', methods=['GET', 'POST'])
def catch_data():
    return render_template('admin/system/catch_data.html')
