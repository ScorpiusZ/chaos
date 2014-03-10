var Facial = { extensions: {} };
Facial.expression = function(converter_options){
	
	//显示表情
	this.showFacial = function(text) {
		// alert("showFacial:"+text);
		text = readFacialXml(text);
		return text;
	};
};


var facialXml = null;

/*读取表情xml文件*/
 function readFacialXml(text){
	if(facialXml)
	{
		return processText(text,facialXml);
	}

	$(document).ready(function(){  
                $.ajax({  
                    url: '/sq/file/fresh_emotion_face.xml',  
                    dataType: 'xml',  
                    type: 'GET',
                    async: false,  
                    timeout: 1000,  
                    error: function(xml){  
         
                        return null;
                    },  
                    success: function(xml){  
                    	facialXml = xml;
                        
                    }  
                });   
            });

    return processText(text,facialXml);
}

/*替换字符串 成 表情图片 html标签*/
 function processText(text,xml){

	$(xml).find("emotions").find("emotion").each(function(index,ele){
             var ch_name = $(ele).attr('ch_name');
             var en_name = $(ele).attr('en_name');
             var facial_text = "<img src='images/"+en_name+".png' width='25px' height='25px'>";

             for(var i=0;i<1000;i++){
             	if(text.indexOf(ch_name)>=0){
             		text=text.replace(ch_name,facial_text);
             	}else{
             		break;
             	}
             }
             
    });

    return text;
}