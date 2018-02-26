function throttle(f, delay){
    var timer = null;
    return function(){
        var context = this, args = arguments;
        clearTimeout(timer);
        timer = window.setTimeout(function(){
            f.apply(context, args);
        },
        delay || 500);
    };
}

$('#drug_search_fields').on('keyup','#drug_name, #drug_strength',throttle(function(){
    let name = $(this).parent().find('#drug_name').val().trim(); // remove any spaces around the text
    let strength = $(this).parent().find('#drug_strength').val().trim();
    if (strength == "") strength = "empty";
    if(name != ""){ // don't make requests with an empty string
        $.ajax({
            url: "search",
            data: {dname: name, dstrength: strength},
            dataType: "json",
            success: function(data){
              $('#results').html(data.results);
            }
        });
    }else{
        $(this).parent().find('#results').html(""); // set the results empty in case of empty string
    }
}));
function add_drug(){
  $('#drug_set').append('<li>'+$('#drug_list option:selected').val()+'</li>');
  $.ajax({
    url: "save_rxcui",
    data: {rxcui: $('#drug_list option:selected').val()},
    dataType: "json",
    success: function(data){
      console.log("sent rxcui "+$('#drug_list option:selected').val()+" to server");
    }
  });
}
function renderDrugSearch(){
  let dsearch =
  `<div class="drug_search">
      <span class="label">Enter Drug Name: </span>
      <input type="text" id="drug_name">
      <span class="label">Enter Drug Strength: </span>
      <input type="text" id="drug_strength">
      <br>
  </div>`
  for(let i = 0; i < $('#numdrugs').val(); i++){
    $('#drug_search_fields').append(dsearch);
  }
}
function get_pdp_region_code(){
    let code = $('#zipcode').val();
    if(code != "" && code.length == 5){
        $.ajax({
            url: "pdp_region_code",
            data: {searchCode: code},
            dataType: "json",
            success: (data) => {
                $("#pdp_region_code").html(data.results);
                $("#enter_drugs").show();
            }
        });
    } else {
        $("#pdp_region_code").html("");
    }
};
function fetch_formularies(){
  $.ajax({
    url: 'formularies',
    data: {},
    dataType: "json",
    success: (data) => {
      $('#formularies').html(data.results);
    }
  });
}
function clear_data(){
  $.ajax({
    url:'clear_data',
    data:{},
    dataType:"json",
    success: (data) => {
      console.log("here");
      $('#results').html("");
      $('#formularies').html("");
      $('#pdp_region_code').html("");
      $('#drug_search_fields').html("");
      $('#drug_set').html("");
    }
  });
}
