from flask import Blueprint, request, make_response, abort

from flask_login import login_required

from gvm.connections import UnixSocketConnection
from gvm.errors import GvmError
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeCheckCommandTransform
from gvm.protocols.gmpv224 import ReportFormatType

from lxml import etree

from markupsafe import escape

from base64 import b64decode

api = Blueprint('api', __name__, url_prefix='/api')

path = '/run/gvmd/gvmd.sock'
connection = UnixSocketConnection(path=path)
transform = EtreeCheckCommandTransform()

# default username with greenbone containers
username = 'admin'

# default password with greenbone containers
# CHANGE ACCORDING TO:
# https://greenbone.github.io/docs/latest/22.4/container/index.html#setting-up-an-admin-user
# AFTER docker compose up -d
password = 'admin'

@api.route("/version")
def get_version():
    with Gmp(connection=connection, transform=transform) as gmp:
        response = gmp.get_version()
        vers = response.xpath('version/text()')[0]
    return {'version': vers}

@api.route("/scanners")
def get_scanners():
    try:
        with Gmp(connection=connection, transform=transform) as gmp:
            gmp.authenticate(username, password)
            response = gmp.get_scanners()
            scanners = response.xpath('scanner/@id')
            names = response.xpath('scanner/name/text()')
        return {'scanners': scanners, 'names': names}
    except GvmError as e:
        abort(500)

@api.route("/configs")
def get_configs():
    try:
        with Gmp(connection=connection, transform=transform) as gmp:
            gmp.authenticate(username, password)
            response = gmp.get_scan_configs()
            ids = response.xpath('config/@id')
            names = response.xpath('config/name/text()')
        return {'configs': ids, 'names': names}
    except GvmError as e:
        abort(500)

@api.route("/port_lists")
def get_port_lists():
    try:
        with Gmp(connection=connection, transform=transform) as gmp:
            gmp.authenticate(username, password)
            response = gmp.get_port_lists()
            ids = response.xpath('port_list/@id')
            names = response.xpath('port_list/name/text()')
        return {'port_lists': ids, 'names': names}
    except GvmError as e:
        abort(500)

@api.route("/targets", methods = ['GET', 'POST'])
def targets():
    if request.method == 'POST':
        request_json = request.json
        if request_json.keys() >= {"name", "hosts", "port_list_id"}:
            try:
                with Gmp(connection=connection, transform=transform) as gmp:
                    gmp.authenticate(username, password)
                    target_id = gmp.create_target(name=request_json['name'], hosts=[request_json['hosts']], port_list_id=request_json['port_list_id']).xpath('@id')
                return {'name': request_json['name'], 'UUID': target_id[0]}
            except GvmError as e:
                abort(500)
        elif request_json.keys() >= {"name", "hosts", "port_range"}:
            try:
                with Gmp(connection=connection, transform=transform) as gmp:
                    gmp.authenticate(username, password)
                    target_id = gmp.create_target(name=request_json['name'], hosts=[request_json['hosts']], port_range=request_json['port_range']).xpath('@id')
                return {'name': request_json['name'], 'UUID': target_id[0]}
            except GvmError as e:
                abort(500)
        elif request_json.keys() >= {"hosts", "port_list_id"}:
            try:
                with Gmp(connection=connection, transform=transform) as gmp:
                    gmp.authenticate(username, password)
                    target_id = gmp.create_target(name=request_json['hosts'] + ' target', hosts=[request_json['hosts']], port_range=request_json['port_list_id']).xpath('@id')
                return {'name': request_json['hosts'] + 'target', 'UUID': target_id[0]}
            except GvmError as e:
                abort(500)
        elif request_json.keys() >= {"hosts", "port_range"}:
            try:
                with Gmp(connection=connection, transform=transform) as gmp:
                    gmp.authenticate(username, password)
                    target_id = gmp.create_target(name=request_json['hosts'] + ' target', hosts=[request_json['hosts']], port_range=request_json['port_range']).xpath('@id')
                return {'name': request_json['hosts'] + 'target', 'UUID': target_id[0]}
            except GvmError as e:
                abort(500)
        elif request_json.keys() >= {"name", "hosts"}:
            try:
                with Gmp(connection=connection, transform=transform) as gmp:
                    gmp.authenticate(username, password)
                    target_id = gmp.create_target(name=request_json['name'], hosts=[request_json['hosts']], port_range='T:1-65535,U:1-65535').xpath('@id')
                return {'name': request_json['name'], 'UUID': target_id[0]}
            except GvmError as e:
                abort(500)
        elif request_json.keys() >= {"hosts"}:
            try:
                with Gmp(connection=connection, transform=transform) as gmp:
                    gmp.authenticate(username, password)
                    target_id = gmp.create_target(name=request_json['hosts'] + ' target', hosts=[request_json['hosts']], port_range='T:1-65535,U:1-65535').xpath('@id')
                return {'name': request_json['hosts'] + 'target', 'UUID': target_id[0]}
            except GvmError as e:
                abort(500)
        else:
            abort(400)
    elif request.method == 'GET':
        try:
            with Gmp(connection=connection, transform=transform) as gmp:
                gmp.authenticate(username, password)
                targets_xml = gmp.get_targets()
            return {'uuids': targets_xml.xpath('target/@id'), 'names': targets_xml.xpath('target/name/text()')}
        except GvmError as e:
            abort(500)

@api.route("/create_task", methods = ['POST'])
def create_task():
    request_json = request.json
    if request_json.keys() >= {"name", "target_id", "config_id", "scanner_id"}:
        try:
            with Gmp(connection=connection, transform=transform) as gmp:
                gmp.authenticate(username, password)
                task_id = gmp.create_task(name=request_json['name'], config_id=request_json['config_id'], target_id=request_json['target_id'], scanner_id=request_json['scanner_id']).xpath('@id')
            return {'UUID': task_id[0]}
        except GvmError as e:
            abort(500)
    elif request_json.keys() >= {"name", "hosts", "config_id", "scanner_id"}:
        try:
            with Gmp(connection=connection, transform=transfrom) as gmp:
                gmp.authenticate(username, password)
                target_id = gmp.create_target(name=request_json['name'] + ' target', hosts=[request_json['hosts']], port_range='T:1-65535,U:1-65535').xpath('@id')
                task_id = gmp.create_task(name=request_json['name'] + ' task', config_id=request_json['config_id'], target_id=target_id, scanner_id=request_json['scanner_id']).xpath('@id')
            return {'UUID': task_id[0]}
        except GvmError as e:
            abort(500)
    elif request_json.keys() >= {"hosts", "config_id", "scanner_id"}:
        try:
            with Gmp(connection=connection, transform=transfrom) as gmp:
                gmp.authenticate(username, password)
                target_id = gmp.create_target(name=request_json['hosts'] + ' target', hosts=[request_json['hosts']], port_range='T:1-65535,U:1-65535').xpath('@id')
                task_id = gmp.create_task(name=request_json['hosts'] + ' task', config_id=request_json['config_id'], target_id=target_id, scanner_id=request_json['scanner_id']).xpath('@id')
            return {'UUID': task_id[0]}
        except GvmError as e:
            abort(500)
    else:
        abort(400)

@api.route("/start_task", methods = ['POST'])
def start_task():
    request_json = request.json
    if request_json.keys() >= {"task_id"}:
        try:
            with Gmp(connection=connection, transform=transform) as gmp:
                gmp.authenticate(username, password)
                response_xml = gmp.start_task(request_json['task_id'])
            return {'status': response_xml.xpath('@status')[0]}
        except GvmError as e:
            abort(500)
    else:
        abort(400)

@api.route("/task_progress/<uuid:task_id>", methods = ['GET'])
def task_progress(task_id):
    try:
        with Gmp(connection=connection, transform=transform) as gmp:
            gmp.authenticate(username, password)
            task_xml = gmp.get_task(escape(task_id))
        return {'status': task_xml.xpath('task/status/text()')[0], 'progress': task_xml.xpath('task/progress/text()')[0]}
    except GvmError as e:
        abort(500)

@api.route("/report_progress/<uuid:report_id>", methods = ['GET'])
def report_progress(report_id):
    try:
        with Gmp(connection=connection, transform=transform) as gmp:
            gmp.authenticate(username, password)
            report_xml = gmp.get_report(escape(report_id))
        return {'progress': report_xml.xpath('report/report/task/progress/text()')[0]}
    except GvmError as e:
        abort(500)

@api.route("/report/<uuid:report_id>.pdf", methods = ['GET'])
def get_report(report_id):
    try:
        with Gmp(connection=connection, transform=transform) as gmp:
            gmp.authenticate(username, password)
            report = gmp.get_report(report_id=escape(report_id), report_format_id=ReportFormatType.PDF)
            content = report.xpath('report/text()')[0]
            pdf_bytes = b64decode(content.encode("ascii"))
            response = make_response(pdf_bytes)
            response.headers.set('Content-Type', 'application/pdf')
            return response
    except GvmError as e:
        abort(500)
