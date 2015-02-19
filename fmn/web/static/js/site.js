var examples_loading_message = "Searching for example messages that match this filter <img src='../../../static/img/spinner.gif'/>";

var load_examples = function(page, endtime) {
    // First, destroy the more button if there is one.
    $('#more-button').remove();

    // Then, get the next page of data from the API (relative url)..
    $.ajax("ex/" + page + "/" + endtime, {
        success: examples_success,
        error: examples_error,
    });
}

var examples_success = function(data, status, jqXHR) {
    var stopping = false;
    if (data.results.length == 0) {
        load_examples(data.next_page, data.endtime);
    } else {
        $('#examples-container .lead').html(
            "The following messages would have matched this filter");
        stopping = true;
    }

    // Put our results on the page.
    $.each(data.results, function(i, meta) {
        var content = "<li class='list-group-item example-message'>";

        if (meta.icon2 != "" && meta.icon2 != null) {
            content = content + "<img src='" + meta.icon2 + "'/>";
        }
        if (meta.icon != "" && meta.icon != null) {
            content = content + "<img src='" + meta.icon + "'/>";
        }

        if (meta.link != "" && meta.link != null) {
            content = content +
                " <a href='" + meta.link + "'>" + meta.time + "</a> ";
        } else {
            content = content + " " + meta.time + " ";
        }

        content = content + "<strong>" + meta.subtitle + "</strong> ";

        content = content + '</li>'

        $('#examples-container .list-group').append(content)
        $('#examples-container .list-group li:last-child').hide();
        $('#examples-container .list-group li:last-child').slideDown('slow');
    });

    // Tack a MOAR button on the end
    if (stopping) {
        var button = '<div id="more-button">' +
            '<button class="btn btn-default btn-lg center-block" ' +
            'onclick="javascript:load_examples(' + data.next_page + ', ' + data.endtime + ');">' +
            '<span class="glyphicon glyphicon-cloud-download"></span>' +
            ' tap for more...' +
            '</button>' +
            '</div>';
        $('#examples-container .list-group').append(button)
        $('#examples-container .list-group div:last-child').hide();
        $('#examples-container .list-group div:last-child').slideDown('slow');
    }
}

var examples_error = function(jqXHR, status, errorThrown) {
    data = jqXHR.responseJSON;
    if (data === undefined) {
        $('#examples-container .lead').html("Unknown error getting examples.");
    } else {
        $('#examples-container .lead').html(data.reason);
    }
    if (data.furthermore != undefined) {
        $('#examples-container').append('<p>' + data.furthermore + '</p>');
    }
    $('#examples-container p').addClass('text-danger');
}

$(document).ready(function() {
    // Kick it off, but only if we're on the right page and there are rules.
    var rules = $("#rules");
    var container = $('#examples-container');
    if (container.length > 0 && rules.children().length > 0) {
        $('#examples-container .lead').html(examples_loading_message);
        var now = Math.floor(new Date().getTime() / 1000.0);
        load_examples(1, now);
    }
});
