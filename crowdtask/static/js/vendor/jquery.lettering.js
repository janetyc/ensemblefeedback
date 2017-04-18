/*global jQuery */
/*!
* Lettering.JS 0.7.0
*
* Copyright 2010, Dave Rupert http://daverupert.com
* Released under the WTFPL license
* http://sam.zoy.org/wtfpl/
*
* Thanks to Paul Irish - http://paulirish.com - for the feedback.
*
* Date: Mon Sep 20 17:14:00 2010 -0600
*/
(function($){
	var constant = 0;
	var start = 1;
	function injector(t, splitter, klass, after) {
		var text = t.text()
		, a = text.split(splitter)
		, inject = '';
		if (a.length) {
			$(a).each(function(i, item) {
				inject += '<span class="'+klass+(constant+i+1)+'" aria-hidden="true">'+item+'</span>'+after;
			});
			t.attr('aria-label',text)
			.empty()
			.append(inject)

		}
		constant += a.length;
	}


	var methods = {
		init : function() {

			return this.each(function() {
				injector($(this), '', 'char', '');
			});

		},

		words : function() {
			var str;
			if ( start == 1 ) {
				str = 'wordOne';
			} else if ( start == 2) {
				str = 'wordTwo';
			}
			return this.each(function() {
				injector($(this), ' ', str, ' ');
			});

		},

		lines : function() {

			return this.each(function() {
				var r = "eefec303079ad17405c889e092e105b0";
				// Because it's hard to split a <br/> tag consistently across browsers,
				// (*ahem* IE *ahem*), we replace all <br/> instances with an md5 hash
				// (of the word "split").  If you're trying to use this plugin on that
				// md5 hash string, it will fail because you're being ridiculous.

				$(this).text($(this).text().replace(/\. /g, ". " + r));
				// $(this).text($(this).text().replace(/! /g, "! " + r));
				// $(this).text($(this).text().replace(/? /g, "? " + r));
				
				if ( start == 1 ) {
					str = 'lineOne';
				} else if ( start == 2) {
					str = 'lineTwo';
				}
				injector($(this).children("br").replaceWith(r).end(), r, str, '');
			});

		}
	};

	$.fn.lettering = function( method , restart ) {
		if ( restart == 2 ) {
			start = 2;
			constant = 0;
		} else {
			start = 1;
			constant = 0;
		}
		// Method calling logic
		if ( method && methods[method] ) {
			return methods[ method ].apply( this, [].slice.call( arguments, 1 ));
		} else if ( method === 'letters' || ! method ) {
			return methods.init.apply( this, [].slice.call( arguments, 0 ) ); // always pass an array
		}
		$.error( 'Method ' +  method + ' does not exist on jQuery.lettering' );
		return this;
	};

})(jQuery);
