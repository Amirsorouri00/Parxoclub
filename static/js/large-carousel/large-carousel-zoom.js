// Large Carousel Zoom

    (function() {
        var $section = $('#focal1');
        var $panzoom = $section.find('#panzoom1').panzoom();
        $panzoom.parent().on('mousewheel.focal1', function(e) {
            e.preventDefault();
            var delta = e.delta || e.originalEvent.wheelDelta;
            var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0;
            $panzoom.panzoom('zoom', zoomOut, {
                animate: false,
                focal: e
            });
        });
    })();


    (function() {
        var $section = $('#focal2');
        var $panzoom = $section.find('#panzoom2').panzoom();
        $panzoom.parent().on('mousewheel.focal2', function(e) {
            e.preventDefault();
            var delta = e.delta || e.originalEvent.wheelDelta;
            var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0;
            $panzoom.panzoom('zoom', zoomOut, {
                animate: false,
                focal: e
            });
        });
    })();


    (function() {
        var $section = $('#focal3');
        var $panzoom = $section.find('#panzoom3').panzoom();
        $panzoom.parent().on('mousewheel.focal3', function(e) {
            e.preventDefault();
            var delta = e.delta || e.originalEvent.wheelDelta;
            var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0;
            $panzoom.panzoom('zoom', zoomOut, {
                animate: false,
                focal: e
            });
        });
    })();