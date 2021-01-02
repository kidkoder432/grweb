from flask import Flask, render_template, request
import os, smtplib
from guessRaga import getRagas
app = Flask(__name__)
from app import routes