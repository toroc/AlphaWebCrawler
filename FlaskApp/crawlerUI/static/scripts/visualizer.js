
/**
 * Global Variables
 */
var nodeColors = [
    '#2C3E50', // Slate
    '#E74C3C', // Watermelon
    '#3498DB', // Sky Blue
    '#2980B9'  // Ocean Blue
];
var colorSwitch = true;
var stage;

/**
 * Resizes the canvas element.
 * @param {Number} width The desired width of the canvas.
 * @param {Number} height The desired height of the canvas.
 */
function resizeCanvas(width, height) {
    var canvas = document.getElementById("demoCanvas");
    canvas.width = width;
    canvas.height = height;
}

/**
 * Makes a display node from web page data.
 * @param {object} page A parsed, individual page returned from the crawler.
 * @param {string} color A hexadecimal color string for the node background
 *     color.
 * @return {Container} A container object containing circle and text
 *     children.
 */
function makeNode(page, color) {
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
 */
function dfsDisplay(stage, pages, nodeColors) {
    var xPos = 170;
    var yPos = 250;
    var colorIdx = 0;
    var pageIdx = 0;

    /**
     * Draws the next node on the canvas.
     */
    function addNodes() {
        if (pageIdx < pages.length) {
            var node = makeNode(pages[pageIdx], nodeColors[colorIdx]);
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
 * @param {NAryTree} pages An N-ary tree of the data.
 * @param {Array} nodeColors An array of hexadecimal color strings.
 */
function bfsDisplay(stage, pages, nodeColors) {
    var xPos = 180;
    var yPos = 180;
    var colorIdx = 0;
    var currentPage = null;
    var childrenPrinted = 0;
    var subTreeNodeCounts = [];
    var children = [pages.root];
    var angleOffset;

    /**
     * Draws the next node to the canvas.
     */
    function addNodes() {
        currentPage = children.shift();
        if (currentPage == pages.root) {
            var node = makeNode(currentPage.element, nodeColors[colorIdx]);
            node.x = xPos;
            node.y = yPos;
            stage.addChild(node);
            stage.update();

            enqueueChildren();
            angleOffset = (Math.PI / 2.0) / subTreeNodeCounts[0];
            updateColor();

        } else if (children.length > 0 && childrenPrinted < subTreeNodeCounts[0]) {
            enqueueChildren();

            var node = makeNode(currentPage.element, nodeColors[colorIdx]);
            var angle = (angleOffset * childrenPrinted);
            console.log("angle: " + angle + " childrenPrinted: " + childrenPrinted);
            calcPolarToCartesianCoords(node, xPos, yPos, 650, angle);
            stage.addChild(node);
            stage.update();

            childrenPrinted++;
            updateColor();
        } else if (children.length > 0) {
            subTreeNodeCounts.shift();
            angleOffset = (Math.PI / 2.0) / subTreeNodeCounts[0];
            childrenPrinted = 0;
        }
    }

    /**
     * Iterates the color index, looping if necessary.
     */
    function updateColor() {
        colorIdx += 1;
        if (colorIdx >= nodeColors.length)
        colorIdx = 0;
    }

    /**
     * Enqueues the current node's children and stores the child count for
     *     that node.
     */
    function enqueueChildren() {
        for (var i = 0; i < currentPage.children.length; i++) {
            children.push(currentPage.children[i]);
        }
        subTreeNodeCounts.push(currentPage.children.length);
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
    var height = isBfs ? 2500 : 500;
    resizeCanvas(4000, height);

    stage = new createjs.Stage("demoCanvas");
    stage.enableMouseOver(10);
    stage.mouseMoveOutside = true;
    if (isBfs) {
        var crawlTree = buildCrawlTree(rawData.visited);
        bfsDisplay(stage, crawlTree, nodeColors);
    } else {
        var orderedData = orderDfsPages(rawData.visited);
        dfsDisplay(stage, orderedData, nodeColors);
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

/**
 * Constructs an N-ary tree of a breadth-first search crawl.
 * @param {Array} pages An array of pages produced from a depth-first search
 *     crawl.
 * @returns {NAryTree} An n-ary tree representing the crawl.
 */
function buildCrawlTree(pages) {
    /**
     * Finds the root page of the crawl and constructs the tree root.
     * @param {Array} pages An array of pages produced from a depth-first
     *     search crawl.
     * @returns {NAryTree} An n-ary tree representing the crawl or null if
     *     the crawl has no root (invalid input).
     */
    function findRoot(pages) {
        for (var i = 0; i < pages.length; i++) {
            if (pages[i].parent === null) {
                var rootNode = new NAryTreeNode(pages[i]);
                pages.splice(i, 1);
                return new NAryTree(rootNode);
            }
        }

        return null;
    }

    /**
     * Recursively finds the children pages of each node in the tree.
     * @param {NAryTreeNode} node The current node in the tree.
     * @param {Array} pages The pages of the crawl.
     * @returns {NAryTreeNode} The node with its children array filled.
     */
    function findChildren(node, pages) {
        // Add all children to current node.
        for (var i = 0; i < pages.length; i++) {
            if (node.element.url === pages[i].parent) {
                var child = new NAryTreeNode(pages[i]);
                node.children.push(child);
                pages.splice(i, 1);
                i--;
            }
        }

        // Base case: no children
        if (node.children.length === 0) {
            return node;
        // Recursive case: find each child nodes children
        } else {
            for (var i = 0; i < node.children.length; i++) {
                findChildren(node.children[i], pages);
            }
            return node;
        }
    }

    var crawlTree = findRoot(pages);
    if (crawlTree) {
        findChildren(crawlTree.root, pages);
    }

    return crawlTree;
}

/** A constructor for an n-ary tree.
 * @param {NAryTreeNode} root The root node of the tree.
 * @constructor
 * @returns {NAryTree} The newly instantiated tree.
 */
function NAryTree(root) {
    this.root = root;

    return this;
}

/**
 * A constructor for an n-ary tree node.
 * @param {object} page The web page to be stored in the tree.
 * @constructor
 * @returns {NAryTreeNode} The newly instantiated tree node.
 */
function NAryTreeNode(page) {
    this.element = page;
    this.parent = null;
    this.children = [];

    return this;
}

/**
 * Adds a childNode to a treeNode.
 * @param {NAryTreeNode} treeNode The node to add as a child.
 * @returns {Number} The new child count of the node.
 */
NAryTreeNode.prototype.addChild = function (treeNode) {
    treeNode.parent = this;
    this.children.push(treeNode);
    return this.children.length;
};

/**
 * Returns the number of children of the node.
 * @returns {Number} The number of children in the calling object.
 */
NAryTreeNode.prototype.childCount = function () {
    return this.children.length;
};
