#!/usr/bin/python
#
# Peteris Krumins (peter@catonmat.net)
# http://www.catonmat.net  --  good coders code, great reuse
#
# The new catonmat.net website.
#
# Code is licensed under GNU GPL license.
#
# This file handles /p/<page_id> short page URLS.

from werkzeug               import Response, redirect, wrap_file
from werkzeug.exceptions    import NotFound

from catonmat.config        import config
from catonmat.models        import Download
from catonmat.database      import session

from catonmat.views.utils           import (
    cached_template_response, render_template, number_to_us
)

# ----------------------------------------------------------------------------

def main(request, filename):
    download = session.query(Download).filter_by(filename=filename).first() 
    if not download:
        # TODO: 'download you were looking for was not found, check out these downloads...'
        raise NotFound()

    try:
        file = open("%s/%s" % (config['download_path'], filename))
    except IOError:
        # TODO: 'the file was not found, check this out'
        raise NotFound()

    download.another_download(request)
    return Response(wrap_file(request.environ, file), mimetype=download.mimetype,
            direct_passthrough=True)


def old_wp_download(request, filename):
    return redirect('/download/%s' % filename, code=301)

def all(request):
    return cached_template_response(
             compute_all,
             'downloads',
             3600)

def compute_all():
    downloads = session. \
      query(Download). \
      order_by(Download.timestamp.desc()). \
      all()
    return render_template('downloads',
        downloads=downloads,
        number_to_us=number_to_us)

