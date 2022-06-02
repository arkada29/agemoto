function load_collection(query)
{
    var search = $('#search_text-1').val()
    var category = $('.selectcategory-1').val()
    var search_data = [
        {query:query}
    ];
    $.ajax({
        url:"/searchcollection",
        method:"POST",
        contentType: "application/json;charset=utf-8",
        traditional: true,
        dataType: 'json',
        data: JSON.stringify(search_data),
        // data:{query2:query2},
        success:function(data)
        {
        $('#result-1').html(data);
        var xmlString = data.htmlresponse//"<input name='token1' type='hidden' value='12345' />"; // Use your xmlHttp.responseText here. This is for demonstration purposes
        var parser = new DOMParser();
        var element = parser.parseFromString(xmlString, "text/html");
        // console.log(element.querySelectorAll('td')[0]);
        // console.log(element.querySelectorAll('td')[1]);
        var le = element.querySelectorAll('td').length
        var result = document.getElementById('result-1')
        var select = document.createElement('select')
        result.appendChild(select)
        select.setAttribute('id', 'selectCollection')
        var selectCollection = document.getElementById('selectCollection')

        var arr = []
        
        for(var i=0;i<le;i++){
            if(element.querySelectorAll('td')[i].value != 'undefined'){   
                arr.push(element.querySelectorAll('td')[i].innerHTML.trim())
                
            }
        }
        arr.unshift('-- select data --')
        // console.log(arr)

        // for(var j = 0;j<arr.length;j++){
        //     var opt  = document.createElement('option')
        //     opt.innerText = arr[j]
        //     select.appendChild(opt)
        // }
        arr.map(function(element, index){
            var opt  = document.createElement('option')
            opt.innerText = arr[index]
            select.appendChild(opt)
        })
        
        function selectIndex(){
            var option = selectCollection.options[selectCollection.selectedIndex];
            document.getElementById('search_text-1').value = option.text
        }

        selectCollection.addEventListener('change', function(){
            selectIndex()
        })
        
        }
        
    });
}
  
function blank(){
    $('#result-1').html('')
}

$('#search_text-1').keyup(function(event){
    var search = $(this).val();
    var category = $('.selectcategory-1').val()
    if(search != ''){
    load_collection(search);
    }
    else{
        blank()
    }
    
});