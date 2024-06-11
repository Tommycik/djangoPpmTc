function white() {
    document.getElementsByClassName("container")[0].style.backgroundColor="black"
}

function cloneMore() {
    var newElement

    newElement = document.getElementsByClassName('item')[0].cloneNode(true);
      // update the management form
    var total=Number($("input[id='id_form-TOTAL_FORMS']").attr('value'))
    let count=total+1
    Number($("input[id='id_form-TOTAL_FORMS']").attr('value',count+""))
    // Updating the input fields are really important and especially the name attributes
    // loop over each input in the new cloning element
    newElement.querySelectorAll("input").forEach(
      function (i, item) {
        //Clear the input’s value
        i.value="";
        let oldName = i.getAttribute("name")
        let oldId = i.getAttribute("id")
        //I’d like to replace the numeric value only with the total value
        //Update the “id and name” attributes of each element
        oldName=oldName.replace(0, total) ;
        oldId=oldId.replace(0, total) ;
        i.setAttribute("name",oldName)
        i.setAttribute("id",oldId)
      })
    // update the delete button index value
    newElement.querySelector("button").setAttribute("onClick",`deleteForm(${length})`)
    // update the span index value
    let spanValue=newElement.querySelector("span").innerHTML.replace(1,`${total+1}`)
    newElement.querySelector("span").innerHTML=spanValue
    newElement.id=`form_num${total}`
    // insert the newElement at the end
    $( newElement ).insertAfter( $(document.getElementsByClassName("item")[total-1]) );
}
function deleteForm(formNum) {
    // Get the current total of forms
    var totalForms = Number($("input[id='id_form-TOTAL_FORMS']").attr('value'))
    // Decrement the totalForms variable by one and update the
    if (totalForms <=1){return}
    totalForms -- ;
    $("input[id='id_form-TOTAL_FORMS']").attr('value', totalForms);
    // Prevent deleting all forms, keep one form
    const collection = document.querySelectorAll(`#form_num${formNum}`)
    for (let i = 0; i < collection.length; i++) {
       collection[i].remove();
    }
    // get all form rows/items by Id
    var forms = $('div[id^="form_num"]')
    for (k = 0; k <= totalForms - 1; k++) {
    let newc=forms[k].querySelector("span").innerHTML="Item"+`${k+1}`+" :";
    forms[k].querySelector("button").setAttribute("onClick",`deleteForm(${k})`)
    let oldId=forms[k].id
    let number_id=oldId.match(/\d+/g);
    forms[k].setAttribute("id",(oldId.replace( number_id, k) ) )
    $(forms.get(k)).find('input').each((j, item) => {
    let oldName = item.getAttribute("name")
    let numberPart=oldId.match(/\d+/g);
    item.setAttribute("name",(oldName.replace(/\d/g, k+"")));
    })
}}