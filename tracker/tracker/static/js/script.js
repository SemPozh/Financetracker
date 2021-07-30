function csrf() {
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '' ) {
			var cookies = document.cookie.split(';');
			for (var i=0; i<cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				if (cookie.substring(0, name.length+1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}

			}
		}
		return cookieValue;
	}

	var csrftoken = getCookie('csrftoken');

	function csrfSafeMethod(method) {
		return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	function sameOrigin(url) {
		var host = document.location.host;
		var protocol = document.location.protocol;
		var sr_origin = '//' + host;
		var origin = protocol + sr_origin;

		return (url == origin || url.slice(0, origin.length + 1) == origin + '/') || (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') || !(/^(\/\/|http:|https:).*/.test(url));
	}

	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
				xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val());
			}
		}
	});
}
















function sidebar() {
	var document_title = $(document).find("title").text();
	
	var sidebar_lis = $('.sidebar').find('.list-group-item');

	if (document_title == 'FinanceTracker') {
		$(sidebar_lis[1]).removeClass('active').removeAttr('aria-current');
		$(sidebar_lis[2]).removeClass('active').removeAttr('aria-current');
		$(sidebar_lis[3]).removeClass('active').removeAttr('aria-current');

		$(sidebar_lis[0]).addClass('active').attr('aria-current', true);
	}

	if (document_title == 'Мои Финансы') {
		$(sidebar_lis[0]).removeClass('active').removeAttr('aria-current');
		$(sidebar_lis[2]).removeClass('active').removeAttr('aria-current');
		$(sidebar_lis[3]).removeClass('active').removeAttr('aria-current');

		$(sidebar_lis[1]).addClass('active').attr('aria-current', true);
	}

	if (document_title == 'Статистика') {
		$(sidebar_lis[0]).removeClass('active').removeAttr('aria-current');
		$(sidebar_lis[1]).removeClass('active').removeAttr('aria-current');
		$(sidebar_lis[3]).removeClass('active').removeAttr('aria-current');

		$(sidebar_lis[2]).addClass('active').attr('aria-current', true);
	}

	if (document_title == 'Отзывы') {
		$(sidebar_lis[0]).removeClass('active').removeAttr('aria-current');
		$(sidebar_lis[1]).removeClass('active').removeAttr('aria-current');
		$(sidebar_lis[2]).removeClass('active').removeAttr('aria-current');

		$(sidebar_lis[3]).addClass('active').attr('aria-current', true);
	}	
}

function show_stars(stars_count) {
	let deactive_stars = 5 - stars_count
	var result = ''
	var i = 0
	while (i < stars_count) {
		result += '<i class="fas fa-star active"></i>';
		i++;
	}

	var j = 0
	while (j < deactive_stars) {
		result += '<i class="far fa-star deactive"></i>';
		j++;
	}

	return result
}


function load_more_reviews() {
	$('#load-more').on('click', function(){
		let lastPostId = $('.last-post').attr('data-postid');
		let data = {
			lastPostId: lastPostId
		}

		$('.review-card').removeClass('last-post');
		$('.review-card').removeAttr('data-postid');


		$.ajax({
			method: 'GET',
			dataType: 'json',
			url: "/load-more-reviews/",
			data: data,
			success: function(data){
				let result = data['data'];
				if(!result){
					$('.load-more').css('display', 'none')
				} else {
					$.each(result, function(key, obj){
						if (obj['last_post']){
							$('.allreviews').append('<div class="review-card mb-3 shadow-sm last-post" data-postid="' + obj['id'] + '">' +
								'<div class="review-info">\
								<div class="review-user">' + 
								obj['user'] + 
								'</div>\
								<div class="review-date">' + 
								obj['date'] +
								'</div>\
								</div>\
								<div class="review-main">\
								<div class="review-grade">' +
								show_stars(obj['grade']) +
								'</div>\
								<div class="review-content">' + 
								obj['content'] +
								'</div>\
								</div>\
								</div>'
								)
						} else{
							$('.allreviews').append('<div class="review-card mb-3 shadow-sm">\
								<div class="review-info">\
								<div class="review-user">' + 
								obj['user'] + 
								'</div>\
								<div class="review-date">' + 
								obj['date'] +
								'</div>\
								</div>\
								<div class="review-main">\
								<div class="review-grade">' +
								show_stars(obj['grade']) +
								'</div>\
								<div class="review-content">' + 
								obj['content'] +
								'</div>\
								</div>\
								</div>'
								)
						}

					})
				}

			}
		})
	})
}


function delete_finance(){
	$('.cross-icon').each((index, el) =>{
		$(el).on('click', (e) => {
			e.preventDefault();

			var finance_id = $(el).attr('delete_id');
			
			$.ajax({
				url: '/delete_finance/',
				type: 'POST',
				data : {
					finance_id: finance_id
				},

				success: (data) =>{
					console.log(data);

					$('#' + finance_id).remove();
				}
			})
		});
	});		
}



function show_finance_data() {
	$('.edit-icon').each((index, el) =>{
		$(el).on('click', (e) => {
			e.preventDefault();


			var redact_id = $(el).attr('redact_id');

			var is_red_income = $('#' + redact_id).find('[name="redact_form"]').find('[name="is_income"]').attr('value');



			let redact_date = $('#' + redact_id).find('.income-date').attr('data-value').replace(' ', '-').replace('г.', '').replace(' ', '-').replace('января', '01').replace('февраля', '02').replace('марта', '03').replace('апреля', '04').replace('мая', '05').replace('июня', '06').replace('июля', '07').replace('августа', '08').replace('сентября', '09').replace('октября', '10').replace('ноября', '11').replace('декабря', '12');
			let year = redact_date.slice(6);
			let month = redact_date.slice(3, 5);
			let day = redact_date.slice(0, 2)
			
			final_date = (year + '-' + month + '-' + day).replace(' ', '')



			let redact_title = $('#' + redact_id).find('.income-title').attr('data-value');
			let redact_money = $('#' + redact_id).find('.income-money').attr('data-value').replace(',', '.');
			let redact_description = $('#' + redact_id).find('.income-description').attr('data-value');


			if (is_red_income == "True"){
				var redact_form = $('.redact_form3_' + redact_id)[0];
				console.log(redact_form);

				var input1 = $(redact_form).find('[name="form3-title"]')[0];
				$(input1).attr('value', redact_title);

				var input2 = $(redact_form).find('[name="form3-money"]');
				$(input2).attr('value', redact_money);

				var input3 = $(redact_form).find('[name="form3-date"]');
				$(input3).attr('value', final_date);

				var input4 = $(redact_form).find('[name="form3-description"]').empty();
				$(input4).append(redact_description);
			} else {
				var redact_form = $('.redact_form4_' + redact_id);

				var input1 = $(redact_form).find('[name="form4-title"]');
				$(input1).attr('value', redact_title);

				var input2 = $(redact_form).find('[name="form4-money"]');
				$(input2).attr('value', redact_money);

				var input3 = $(redact_form).find('[name="form4-date"]');
				$(input3).attr('value', final_date);

				var input4 = $(redact_form).find('[name="form4-description"]').empty();
				$(input4).append(redact_description);
			}




		})
	});
}


function redact_finance(){
	$('[name="redact_form"]').each((index, el) =>{
		$(el).on('submit', (e) => {
			e.preventDefault();



			var is_income = $(el).find('[name="is_income"]').attr('value');
			var finance_red_id = $(el).find('[name="is_income"]').attr('data_financeId');

			if (is_income == "True") {
				var redacted_title = $(el).find('#id_form3-title').val();
				var redacted_money = $(el).find('#id_form3-money').val();
				var redacted_date = $(el).find('#id_form3-date').val();
				var redacted_description = $(el).find('#id_form3-description').val();
			} else {
				var redacted_title = $(el).find('#id_form4-title').val();
				var redacted_money = $(el).find('#id_form4-money').val();
				var redacted_date = $(el).find('#id_form4-date').val();
				var redacted_description = $(el).find('#id_form4-description').val();
			}

			
			$.ajax({
				method: 'POST',
				dataType: 'json',
				url: '/redact_finance/',
				data: {
					finance_red_id: finance_red_id,
					redacted_title: redacted_title,
					redacted_money: redacted_money,
					redacted_date: redacted_date,
					redacted_description: redacted_description,
				},

				success: (data) =>{
					var redact_card = $('#' + data['id']);
					console.log(data['date']);

					$(redact_card).find('.income-title').empty().append(data['title']);

					$(redact_card).find('.income-money').empty().append(data['money'] + ' р ' + '<i class="fas fa-coins"></i>');

					$(redact_card).find('.income-date').empty().append(data['date']);

					$(redact_card).find('.income-description').empty().append(data['description']);


					$(redact_card).find('.btn-close')[0].click();

				}
			});
		});
	});
}


$(document).ready(() =>{
	csrf();

	sidebar();
	load_more_reviews();
	delete_finance();
	show_finance_data();
	redact_finance();
});