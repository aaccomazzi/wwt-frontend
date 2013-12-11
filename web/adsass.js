var wwt;

var years = ["date-pre1800_512", "date-1800_1850_512", "date-1850_1900_512", "date-1900_1910_512",
    "date-1910_1920_512", "date-1920_1930_512", "date-1930_1940_512", "date-1940_1945_512", "date-1945_1950_512",
    "date-1950_1955_512", "date-1955_1960_512", "date-1960_1965_512", "date-1965_1970_512", "date-1970_1975_512",
    "date-1975_1980_512", "date-1980_1985_512", "date-1985_1990_512", "date-1990_512", "date-1991_512",
    "date-1992_512", "date-1993_512", "date-1994_512", "date-1995_512", "date-1996_512", "date-1997_512",
    "date-1998_512", "date-1999_512", "date-2000_512", "date-2001_512", "date-2002_512", "date-2003_512",
    "date-2004_512", "date-2005_512", "date-2006_512", "date-2007_512", "date-2008_512", "date-2009_512",
    "date-2010_512", "date-2011_512", "date-2012_512", "date-2013_512"
];
var cat = [];
var cat_color = '#ff0000';
var cat_radius = 5;
var cat_visible = false;

function initialize() {
    wwt = wwtlib.WWTControl.initControl("WWTCanvas");
    wwt.add_ready(wwtReady);
    resize_canvas();
}

function getParameter(name) {
    // this next line is why I hate JavaScript
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");

    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);

    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function resize_canvas() {

    div = document.getElementById("WWTCanvas");

    if (div.style.width != (window.innerWidth).toString() + "px") {
        div.style.width = (window.innerWidth).toString() + "px";
    }

    if (div.style.height != (window.innerHeight).toString() + "px") {
        div.style.height = ((window.innerHeight)).toString() + "px";
    }

    $('#sky-location').css({
        'bottom': $('#footer').height() + 20 + 'px'
    });
}


function displayCoordinates(event) {
    var coords = '(α,δ)=' + (wwt.getRA() * 15).toFixed(2) + "°, " + wwt.getDec().toFixed(2) + "° FOV= " + wwt.get_fov().toFixed(0) + "°";
    $('#sky-location').text(coords);
}

function _gotoSimbadResult(data) {
    console.log(data);
    if (data.substr(0, 7) == '::error') return false;
    var result = data.split(' ');
    if (result.length != 2) return false;
    var ra = parseFloat(result[0]),
        dec = parseFloat(result[1]);
    if (isNaN(ra) || isNaN(dec)) return false;

    wwt.gotoRaDecZoom(ra, dec, wwt.get_fov(), true);
    return true;
}

function gotoQuery(query) {
    var simbad_url = 'http://simbad.harvard.edu/simbad/sim-script';
    var script = 'output script=off\noutput console=off\noutput error=off\n format object form1 "%COO(d;A) %COO(d;D)"\nquery id ' + query;

    var squery = query.split(' ');
    if (squery.length == 2) {
        var ra=parseFloat(squery[0]), dec=parseFloat(squery[1]);
        if (!isNaN(ra) && !isNaN(dec)) {
            wwt.gotoRaDecZoom(ra, dec, wwt.get_fov(), true);
            $('#goto-query').attr('placeholder', 'Go to...');
            return;
        }
    }

    $.ajax({
            url: simbad_url,
            type: "POST",
            data: {
                'submit': 'submit script',
                'script': script
            },
            success: function(data) {
                if (!_gotoSimbadResult(data)) {
                    $('#goto-query').attr('placeholder', 'invalid').val('');
                    return;
                }
                $('#goto-query').attr('placeholder', 'Go to...');
            }
    });
}


function finderScope(parent, obj) {
    var simbad_url = 'http://simbad.u-strasbg.fr/simbad/sim-id?Ident=' + encodeURIComponent(obj.id);

    var url = 'http://simbad.harvard.edu/simbad/sim-script';
    var script = 'output script=off\noutput console=off\noutput error=off\nformat object f1 "%BIBCODELIST(R;;1000;%B | %1A | %J)"';
    script += '\nquery ' + obj.id;

    $.ajax({
        url: url,
        type: "POST",
        data: {
            'submit': 'submit script',
            'script': script
        },
        success: function(data) {
            var output = '<h4> Papers </h4>';
            uresult = data.split(/\r?\n/);
            //uresult = unique(result);
            var biblist = [];
            truncated = false;

            //trim list of papers to 120 to avoid URL too long to fail
            if (uresult.length > 201) {
                truncated = true;
                paper_length = 201;
            } else {
                paper_length = uresult.length;
                truncated = false;
            }

            if (truncated) {
                output += "<p class='small text-danger'>Note: List truncated to 200 papers</p>";
            }


            for (var i = 0; i < paper_length; i++) {
                if ( !! uresult[i]) {
                    output += '<a target="_blank" href="http://adsabs.harvard.edu/abs/' + encodeURIComponent(uresult[i].split('|')[0]) + '">' + uresult[i].split('|')[1].trim() + ' ' + uresult[i].split('|')[2].trim() + '</a><br>';
                    biblist.push(encodeURIComponent(uresult[i].split('|')[0]));
                }
            }

            biblist = biblist + "";
            biblist = biblist.replace(/\,/g, 'OR%20');
            biblist = 'http://labs.adsabs.harvard.edu/ui/cgi-bin/topicSearch?q=bibcode:(' + biblist + ')';

            buttons = "<a class='btn btn-default' type='button' target='_blank' href='" + simbad_url + "'> SIMBAD Entry </a>";
            buttons += '&nbsp; <a class="btn btn-default" type="button" target="_blank" href="' + biblist + '"> Open papers in ADS </a>';

            $('#finderscope-label').html(obj.id + " " + buttons);
            $('#finderscope .modal-body').html(output);
            $("#finderscope").modal('show');
        }
    });
}

function wwtReady() {

    wwt.settings.set_showCrosshairs(true);
    wwt.settings.set_showConstellationFigures(false);
    wwt.hideUI(true);
    wwt.settings.set_showConstellationBoundries(false);
    // Load in the image collection file
    wwt.loadImageCollection("/adsass.wtml");

    wwt.add_collectionLoaded(default_layers);
    wwt.add_annotationClicked(finderScope);

    $("#WWTCanvas").mousemove(displayCoordinates);
    $("#WWTCanvas").scroll(function(e) {
        e.preventDefault();
    });

    $.getJSON('simbad.json', function(data) {
        for (var i = 0; i < data.length; i++) {
            var circle = wwt.createCircle(true);
            circle.set_lineColor(cat_color);
            circle.set_fillColor(cat_color);
            circle.set_lineWidth(0);
            circle.set_opacity(0.8);
            circle.set_radius(cat_radius);
            circle.setCenter(data[i]['ra'], data[i]['dec']);
            circle.set_label(data[i]['name']);
            circle.set_id(data[i]['name']);
            circle.set_showHoverLabel(true);
            cat.push(circle);
        }
    });

    $('#WWTCanvas').mouseout(function(e) {
        wwtlib.WWTControl.singleton.onMouseUp(e);
    });

}

function showCatalog() {
    cat_visible = true;
    for (var i = 0; i < cat.length; i++) wwt.addAnnotation(cat[i]);
}

function hideCatalog() {
    cat_visible = false;
    wwt.clearAnnotations();
}

function toggleCatalog() {
    if (cat_visible) {
        hideCatalog();
    } else {
        showCatalog();
    }
}

function default_layers() {
    var ra = parseFloat(getParameter('ra') || '0');
    var dec = parseFloat(getParameter('dec') || '0');
    var fov = parseFloat(getParameter('fov') || '60');
    var layer = (getParameter('layer') || 'allSources');
    if (layer.slice(layer.length - 4) !== '_512')
        layer = layer + '_512';

    wwt.setForegroundImageByName(layer);

    $('#facet-list a').each(function(i, o) {
        if ($(o).attr('href') == layer) {
            o.click();
            $('#foreground-lbl').text($(o).text());
            return;
        }
    });


    setBackground("WISE", "WISE");
    wwt.setForegroundOpacity(50);

    wwt.gotoRaDecZoom(ra, dec, fov, true);
}

function setBackground(name, label) {
    wwt.setBackgroundImageByName(name);
    $('#background-lbl').text(label);
}

function setForeground(layer, label) {
    wwt.setForegroundImageByName(layer);
    wwt.setForegroundOpacity($("#slider-opacity").slider("option", "value"));
    $('#foreground-lbl').text(label);
}

function deslectFacets() {
    //update highlight
    $("#facet-list a").each(function(index) {
        $(this).attr('class', '');
    });
    $("#year-label").hide();
}

$(function() {

    $("#year-label").hide();

    $("#slider-opacity").slider({
        min: 0,
        max: 100,
        value: 50,
        slide: function(event, ui) {
            wwt.setForegroundOpacity(ui.value);
        }
    });

    $("#toggle-list a").click(function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        setBackground(url, $(this).text());

        //update highlight
        $("#toggle-list a").each(function(index) {
            $(this).attr('class', '');
        });
        $(this).attr('class', 'label label-default');
    });

    $("#facet-list a").click(function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        setForeground(url, $(this).text());
        deslectFacets();
        $(this).attr('class', 'label label-default');
    });

    $("#slider-year").slider({
        min: 0,
        max: years.length - 1,
        value: years.length / 2,
        slide: function(event, ui) {
            var layer = years[ui.value];
            var display = layer.slice(5, layer.length - 4);

            deslectFacets();
            setForeground(layer, display);
            $("#year-label").show().text(display);
        }
    });

    $("#button-source").click(toggleCatalog);

    $('#WWTCanvas').bind('mousewheel DOMMouseScroll', function(e) {
        e.preventDefault();
    });

    $('#aladin-link').click(function(e) {
        e.preventDefault();
        var ra = wwt.getRA() * 15,
            dec = wwt.getDec(),
            fov = wwt.get_fov(),
            layer = wwtlib.WWTControl.singleton.renderContext.get_foregroundImageset().$16;

        layer = layer.slice(0, layer.length - 4); // strip off _512
        var url = $('#aladin-link').attr('href') + '?ra=' + ra + '&dec=' + dec +
            '&fov=' + fov + '&layer=' + layer;
        window.open(url);
    });

    $('#btn-goto').click(function(e) {
        var query = $('#goto-query').val();
        gotoQuery(query);
    });

    $('#goto-query').keyup(function(e) { // listen to enter key
        if (e.keyCode != 13) return;
        var query = $(this).val();
        gotoQuery(query);
    });

    $('#base-list a, #facet-list a').tooltip({
        'placement': 'bottom',
        'delay': 500
    });

    $('#footer').click(function(e){$('#footer .detail').show(100);});

    $("#footer").hover(function(e){}, function(e) {
        $('#footer .detail').hide(100);
    });
});