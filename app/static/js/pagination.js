const path = location.href
const pageList = document.querySelectorAll('.page-item')
const pageA = document.querySelectorAll('.page-item a')
const pageLink = document.querySelectorAll('.numbered')
const pageLength = pageA.length

var firstPageLink = pageLink[0];
firstPageLink.style.cssText += 'background:blueviolet;\
                                color:white;\
                                postion:absolute;\
                                bottom:10px';

for(let i = 0; i<pageLength; i++){
    if(pageA[i].href == path){
    pageList[i].classList.add('hovered')
    var attr = pageList[i].getAttribute('class')
    console.log(path)
    if( attr.includes('hovered') == true){
        firstPageLink.style.cssText = ''
    }
    if(String(path).includes('page=1') == true){
        firstPageLink.style.cssText += 'background:blueviolet;\
                                color:white;\
                                postion:absolute;\
                                bottom:10px';
    }
    // console.log(pageList[i].getAttribute('class'))
    }
}