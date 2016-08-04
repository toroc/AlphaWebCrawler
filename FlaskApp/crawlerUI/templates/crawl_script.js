$(document).ready(function(){
	var crawls = JSON.parse(localStorage.getItem("savedCrawls"));
	if (crawls != null){
		var sel = $('<select>').appendTo('#previous');
		for (c in crawls){
			sel.append($("<option>").text("URL:"+crawls[c]['url']+ " Crawl Type: "+crawls[c]['crawl-type']).attr('value', c));
		}

		var past_button = $('<button>').appendTo('#previous');
		past_button.text("Crawl Again");

		past_button.click(function(event){
			var curIndex = sel.val();
			var targetCrawl = crawls[curIndex];
			console.log(JSON.stringify(targetCrawl));
			$.ajax({
				url: 'http://alpha-crawler.appspot.com/',
				type: 'POST',
				crossDomain: true,
				dataType: "url",
				data : targetCrawl,
				success: function(result){
					console.log(result);
				},
				error: function(xhr, resp, text){
					console.log(xhr, resp, text);
				}
			})

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
