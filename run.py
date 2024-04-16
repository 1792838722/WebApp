from waitress import serve
from chart.wsgi import application

serve(
    app=application,
    host='127.0.0.1',
    port=8000
)
