
/**
 * Global Variables
 */
var nodeColors = [
    '#2C3E50', // Slate
    '#E74C3C', // Watermelon
    '#3498DB', // Sky Blue
    '#2980B9'  // Ocean Blue
];
var textColor = '#ECF0F1'; // Ice White
var colorSwitch = true;
var stage;

/**
 * Expands the canvas element to fit the window size.
 */
function makeCanvasFullScreen() {
    var canvas = document.getElementById("demoCanvas");
    canvas.width = 4000;
    canvas.height = 2500;
}

/**
 * Makes a display node from web page data.
 * @param {object} page A parsed, individual page returned from the crawler.
 * @param {string} color A hexadecimal color string for the node background
 *     color.
 * @param {string} textColor A hexadecimal color string for the text color.
 * @return {Container} A container object containing circle and text
 *     children.
 */
function makeNode(page, color, textColor) {
    /**
     * An event handler to open the associated webpage on click.
     * @param {Event} event The event object supplied to the handler.
     */
    function handleClick(event) {
        window.open(page['url'], '_blank');
    }

    /**
     * Zooms in on node on rollover.
     * @param {Event} event The event object supplied to the handler.
     */
    function rolloverZoom(event) {
        event.target.scaleX = event.target.scaleY = event.target.scale * 1.8;
        stage.update();
    }

    /**
     * Zooms out from node on rollout.
     * @param {Event} event The event object supplied to the handler.
     */
    function rolloutZoom(event) {
        event.target.scaleX = event.target.scaleY = event.target.scale;
        stage.update();
    }

    var circle = new createjs.Shape();
    var text = new createjs.Text(cleanTitle(page['title']), '14px Arial');

    circle.graphics.beginFill(color).drawCircle(0, 0, 20);
    text.color = color;
    text.x = -90;
    text.y = 30;
    text.lineWidth = 180;

    var container = new createjs.Container();
    container.cursor = "pointer";
    container.scale = 1.0;
    container.addChild(circle, text);
    container.on("click", handleClick);
    container.on("rollover", rolloverZoom);
    container.on("rollout", rolloutZoom);

    return container;
}

/**
 * Draws a depth-first search visualization to the document canvas.
 * @param {Stage} stage The stage object associated with the canvas.
 * @param {Array} pages An ordered array of page objects.
 * @param {Array} nodeColors An array of hexadecimal color strings.
 * @param {String} textColor A hexadecimal color string
 */
function dfsDisplay(stage, pages, nodeColors, textColor) {
    var xPos = 100;
    var yPos = window.innerHeight / 2;
    var colorIdx = 0;
    var pageIdx = 0;

    /**
     * Draws the next node to the canvas.
     */
    function addNodes() {
        if (pageIdx < pages.length) {
            var node = makeNode(pages[pageIdx], nodeColors[colorIdx], textColor);
            node.x = xPos;
            node.y = yPos;
            stage.addChild(node);
            stage.update();

            xPos += 200;
            pageIdx += 1;
            colorIdx += 1;
            if (colorIdx >= nodeColors.length)
            colorIdx = 0;
        }
    }

    createjs.Ticker.interval = 500;
    createjs.Ticker.addEventListener("tick", addNodes);
}

/**
 * Draws a breadth-first search visualization to the document canvas.
 * @param {Stage} stage The stage object associated with the canvas.
 * @param {object} pages The parsed JSON page data.
 * @param {Array} nodeColors An array of hexadecimal color strings.
 * @param {String} textColor A hexadecimal color string
 */
function bfsDisplay(stage, pages, nodeColors, textColor) {
    var xPos = window.innerWidth / 2;
    var yPos = window.innerHeight / 2;
    var colorIdx = 0;
    var pageIdx = 0;
    var childIdx = 0;
    var children = pages['visited'].length;
    var angleOffset = (2 * Math.PI) / children;

    /**
     * Draws the next node to the canvas.
     */
    function addNodes() {
        if (pageIdx == 0) {
            var node = makeNode(pages['visited'][pageIdx], nodeColors[colorIdx], textColor);
            node.x = xPos;
            node.y = yPos;
            stage.addChild(node);
            stage.update();

            pageIdx += 1;
            colorIdx += 1;
            if (colorIdx >= nodeColors.length)
            colorIdx = 0;

        } else if (pageIdx < pages['visited'].length) {
            var node = makeNode(pages['visited'][pageIdx], nodeColors[colorIdx], textColor);
            calcPolarToCartesianCoords(node, xPos, yPos, 250, angleOffset * childIdx);
            stage.addChild(node);
            stage.update();

            pageIdx += 1;
            childIdx += 1;
            colorIdx += 1;
            if (colorIdx >= nodeColors.length)
            colorIdx = 0;
        }
    }

    createjs.Ticker.interval = 500;
    createjs.Ticker.addEventListener("tick", addNodes);
}

/**
 * Positions a node on the canvas using polar coordinates.
 * @param {Container} node The graphics node to be positioned.
 * @param {Number} xPos The x-coordinate to be offset from.
 * @param {Number} yPos The y-coordinate to be offset from.
 * @param {Number} distance The distance in pixels to be offset from xPos and
 *     yPos.
 * @param {Number} angle The angle at which to be offset from xPos and yPos.
 */
function calcPolarToCartesianCoords(node, xPos, yPos, distance, angle) {
    node.x = xPos + (distance * Math.cos(angle));
    node.y = yPos + (distance * Math.sin(angle));
}

/**
 * Initializes the graphics stage and starts the visualization.
 */
function init() {
    makeCanvasFullScreen();

    stage = new createjs.Stage("demoCanvas");
    stage.enableMouseOver(10);
    stage.mouseMoveOutside = true;
    if (isBfs) {
        bfsDisplay(stage, rawData, nodeColors, textColor);
    } else {
        var orderedData = orderDfsPages(rawData.visited);
        dfsDisplay(stage, orderedData, nodeColors, textColor);
    }

}

init();

/**
 * Removes leading and trailing braces/quotation marks from title string.
 * @param {String} title A title string with header and trailer characters.
 * @return {String} The cleaned-up string.
 */
function cleanTitle(title) {
    return title.substring(2, title.length-2);
}

/**
 * Constructs a linear ordering of the pages in a depth-first search.
 * @param {Array} pages An unordered array of the pages in a depth-first
 *     search.
 * @return {Array} An ordered array of the pages in a depth-first search.
 */
function orderDfsPages(pages) {
    var orderedPages = [];

    // Find root page
    for (var i = 0, rootFound = false; i < pages.length && !rootFound; i++) {
        if (pages[i].parent === null) {
            orderedPages.push(pages[i]);
            pages.splice(i, 1); // remove parent
            rootFound = true;
        }
    }

    // Build list of children
    while (pages.length) {
        for (var i = 0; i < pages.length; i++) {
            if (pages[i].parent === orderedPages[orderedPages.length-1].url) {
                orderedPages.push(pages[i]);
                pages.splice(i, 1);
                break;
            }
        }
    }

    return orderedPages;
}

/****************************************************************/

function DepthFirstList(crawlData) {



    return this;
}

function BreadthFirstTree() {

}
