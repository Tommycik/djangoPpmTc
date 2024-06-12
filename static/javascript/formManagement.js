function white() {
    document.getElementsByClassName("container")[0].style.backgroundColor="black"
}

let categories = 0;
let ingredients=0
let newIngredients=0
let steps=0
function cloneMore(element='ingredient') {
    let newElement;

    newElement = document.getElementsByClassName(element)[0].cloneNode(true);
      // update the management form
    var total=Number($("input[id='id_form-TOTAL_FORMS']").attr('value'))
    let count=total+1
    Number($("input[id='id_form-TOTAL_FORMS']").attr('value',count+""))
    let items=ingredients
    if(element==='ingredient'){
        ingredients++
        items=ingredients
    }else if(element==='newIngredient'){
        newIngredients++
        items=newIngredients
    }else if(element==='category'){
        categories++
        items=categories
    }else if(element==='steps'){
        steps++
        items=steps
    }



    // Updating the input fields are really important and especially the name attributes
    // loop over each input in the new cloning element
    /*newElement.querySelectorAll("input").forEach(
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
      })*/
    // update the delete button index value
    newElement.querySelector("button").setAttribute("onClick",`deleteForm(${items},'${element}')`)
    // update the span index value
    let spanValue=newElement.querySelector("span").innerHTML.replace(1,`${items+1}`)
    newElement.querySelector("span").innerHTML=spanValue
    newElement.id=element+`${total}`
    // insert the newElement at the end
    $( newElement ).insertAfter( $(document.getElementsByClassName(element)[`${items-1}`]) );
}
function deleteForm(formNum,element='ingredient') {
    // Get the current total of forms
    var totalForms = Number($("input[id='id_form-TOTAL_FORMS']").attr('value'))
    let number
    // Decrement the totalForms variable by one and update the
    if(element==='ingredient'){
        number=ingredients
    }else if(element==='newIngredient'){
        number=newIngredients
    }else if(element==='category'){
        number=categories
    }else if(element==='steps'){
        number=steps
    }
    if (number <=0){return}
    totalForms -- ;
    number--
    $("input[id='id_form-TOTAL_FORMS']").attr('value', totalForms);
    if(element==='ingredient'){
        ingredients--
    }else if(element==='newIngredient'){
        newIngredients--
    }else if(element==='category'){
        categories--
    }else if(element==='steps'){
        steps--
    }
    // Prevent deleting all forms, keep one form
    const collection = document.querySelectorAll(`#${element}${formNum}`)

    for (let i = 0; i < collection.length; i++) {
       collection[i].remove();
    }
    let forms= document.querySelectorAll(`[id^=${element}]`)
    for (k = 0; k <= number; k++){
        forms[k].querySelector("span").innerHTML=`${element}${k+1}`+" :";
        forms[k].querySelector("button").setAttribute("onClick",`deleteForm(${k},'${element}')`)
        forms[k].setAttribute('id',element+`${k}`)
    }
    // get all form rows/items by Id
   /* var forms = $('div[id^=element]')
    for (k = 0; k <= number - 1; k++) {
    let newc=forms[k].querySelector("span").innerHTML=element +`${k+1}`+" :";
    forms[k].querySelector("button").setAttribute("onClick",`deleteForm(${k})`)
    let oldId=forms[k].id
    let number_id=oldId.match(/\d+/g);
    forms[k].setAttribute("id",(oldId.replace( number_id, k) ) )
    $(forms.get(k)).find('input').each((j, item) => {
    let oldName = item.getAttribute("name")
    let numberPart=oldId.match(/\d+/g);
    item.setAttribute("name",(oldName.replace(/\d/g, k+"")));
    })
}*/
}