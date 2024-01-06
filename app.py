import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'])

server = app.server
app.config.suppress_callback_exceptions = True

