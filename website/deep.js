function getGrid(select){
	var gridSize = select.value
	$('.shoes').empty();
	liked = []

	$.post({
		url: 'https://xkv8t7uwu2.execute-api.us-east-1.amazonaws.com/api/',
		data: JSON.stringify({'grid_size': gridSize}),
		success: function ( data ) {
			for (i = 0; i < gridSize; i++) {
				url = 'https://s3.amazonaws.com/deepheels/img/' + data["grid"][i] + '.jpg'
				$('.shoes').append(`
					<div 
					class = "box" 
					style = "background-image : url( ${url} )" 
					data-id = ${data["grid"][i]}>
					<i></i>
					</div>`)
			}
		}
	})
}

getGrid({value: "5"})

$(document).on('click', 'i', function() { 
	var like = $(this).parent().data('id')
	$(this).css( { "color": "#F00" } )

	if (!liked.includes(like)) {
		liked.push(like)
	}

	var grid = []
	$('.box').each(function () {
		grid.push($(this).data('id'))
	})

	var data = {
		like : like,
		liked : liked,
		grid : grid
	}

	$.post({
		url: 'https://2w4q7c6yaj.execute-api.us-east-1.amazonaws.com/api/',
		data: JSON.stringify(data),
		success: function ( data ) {
			for (i = 0; i < data['changes'].length; i++) {
				url = 'https://s3.amazonaws.com/deepheels/img/' + data['changes'][i]['id'] + '.jpg'
				$(`.box:eq(${data['changes'][i]['position']})`).css( { "background-image": `url( ${url}` } )
				$(`.box:eq(${data['changes'][i]['position']})`).data('id', data['changes'][i]['id'] )
			}
		}
	})
})