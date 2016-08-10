$(document).ready(function(){
	var crawls = JSON.parse(localStorage.getItem("savedCrawls"));
	if (crawls != null){
		var sel = $('<select>').appendTo('#crawlHist');
		for (c in crawls){
			sel.append($("<option>").text("URL:"+crawls[c]['url']+ " Crawl Type: "+crawls[c]['crawl-type']).attr('value', c));
		}

		var past_button = $('<button>').appendTo('#crawlHist');
		past_button.text("Crawl Again");

		past_button.click(function(event){
			var curIndex = sel.val();
			var targetCrawl = crawls[curIndex];
			console.log(JSON.stringify(targetCrawl));
			var url ='/crawl';
			var method= 'post';

			var past_search = $('<form>', {
				action: url,
				method: method
			});

			$('<input>').attr({
				type: "hidden",
				name: 'url',
				value: targetCrawl['url']
			}).appendTo(past_search);

			$('<input>').attr({
				type: "hidden",
				name: 'crawl-type',
				value: targetCrawl['crawl-type']
			}).appendTo(past_search);

			$('<input>').attr({
				type: "hidden",
				name: 'keyword',
				value: targetCrawl['keyword']
			}).appendTo(past_search);

			$('<input>').attr({
				type: "hidden",
				name: 'limit',
				value: targetCrawl['limit']
			}).appendTo(past_search);

			past_search.submit();
		});
	}
});

$("form").submit(function(event){
	var currentCrawl = {};
	currentCrawl['url'] = $('input[name=url]').val(),
	currentCrawl['crawl-type'] = $('select[name=crawl-type]').val(),
	currentCrawl['keyword'] = $('input[name=keyword]').val(),
	currentCrawl['limit'] = $('input[name=limit]').val(),
	console.log(JSON.stringify(currentCrawl));
	var crawls = JSON.parse(localStorage.getItem("savedCrawls"));
	console.log(JSON.stringify(crawls));
	if (crawls == null){
		crawls = [];
		crawls.push(currentCrawl);
		console.log(JSON.stringify(crawls));
		localStorage.setItem("savedCrawls", JSON.stringify(crawls));
	}else{
		crawls.push(currentCrawl);
		console.log(JSON.stringify(crawls));
		localStorage.setItem("savedCrawls", JSON.stringify(crawls));
	}
});
