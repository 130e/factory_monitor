window.calender = (function(win,doc){
    function C(str){
        this.dom = doc.querySelector(str);
        this.s = {
            date : [ new Date().getFullYear(),new Date().getMonth()+1,new Date().getDate()],
            button : false,
            format : 'yyyy年MM月dd日',
            left : 0,
            top: 0,
            onload : function(){}
        }
    };

    C.prototype = {
        init : function(){
            var t = this;
            if( typeof arguments[0] == 'function'){
            t.cb = arguments[0];
        }else{
            t.newS = arguments[0];
            t.cb = arguments[1] || function(){}
        };
        t.yoff = false;
        t.moff = false;
            t.extend(t.s,t.newS);
            t.nt = new Date();
            t.nt.setFullYear(t.s.date[0]);
            t.nt.setMonth(t.s.date[1]-1);
            var len = this.getDateLength(t.nt.getFullYear(),t.nt.getMonth() )
            t.nt.setDate(t.s.date[2]>len ? len : t.s.date[2]);
            t.day = t.nt.getDate();
            t.dom.onclick = function(ev){
                var e = ev || event;
                t.create();
                t.bind();
                t.s.onload.call(this)
                e.stopPropagation ? e.stopPropagation() : (e.cancelBubble = true)
            };  
        },
        hide : function(){
            var t = this;
            t.cb.call(t.dom,t.format( t.nt.getFullYear()+'/'+ (t.nt.getMonth()+1)+'/'+ t.day+' '+new Date().getHours()+':'+new Date().getMinutes()+':'+new Date().getSeconds(),t.s.format));
            if( g('.calender-wrap')) doc.body.removeChild( g('.calender-wrap') )
        },
        bind : function(){
            var t = this;
            var Content = g('.calender-content');
            t.createDay();
            var Prev = g('#calender-prev'),
                Next = g('#calender-next'),
                Year = g('#calender-year'),
                Mon = g('#calender-mon');
            if(t.s.button){
                var today = g('.calender-today');
                var enter = g('.calender-ent');
                today.onclick = function(){
                    t.nt.setFullYear(new Date().getFullYear());
                    t.nt.setMonth(new Date().getMonth());
                    t.nt.setDate( new Date().getDate());
                    t.s.date[2] = t.day = new Date().getDate()
                    t.createYear()
                    t.createDay()
                    t.createMon()
                };
                enter.onclick = function(){
                    t.hide();
                }
            }
            Content.onclick = function(ev){
                var ev = ev || event; 
            var _target = ev.target || ev.srcElement; 
            if(!t.has(_target,'calender-cell-dark') ){
                var chl = this.children;
                for(var i = 0;i<chl.length;i++){
                    t.del(chl[i],'active');
                };
                t.add(_target,'active');
                t.nt.setDate(_target.getAttribute('data-n'));
                t.s.date[2] = t.day = _target.getAttribute('data-n')
                if(!t.s.button){
                    t.hide();
                }
            }
            }
            Prev.onclick = Next.onclick = function(){
                var y = t.nt.getFullYear(),m = t.nt.getMonth();
                if(t.moff) return
                if(t.yoff){
                    t.nt.setFullYear( this.id=="calender-prev" ? y -= 9 : y += 9)
                    t.createYear()
                }else{
                    this.id=="calender-prev" ? m-- : m++;
                    t.nt.setDate(1);
                    t.nt.setMonth( m );
                    t.createDay()
                }
            }
            Year.onclick = function(){
                t.createYear();
                t.yoff = true;
                t.moff = false;
                t.del(g('.calender-wrap'),'month');
                t.add(g('.calender-wrap'),'year');
            };
            Mon.onclick = function(){
                t.createMon();
                t.moff = true;
                t.yoff = false;
                t.del(g('.calender-wrap'),'year');
                t.add(g('.calender-wrap'),'month');
            };
        },
        getDateLength : function(year,month){
            //获取某一月有多少天, month为实际月份，一月即为1
            return new Date(year,month,0).getDate();
        },
        getFirstDay : function(year,month){
            //获取某一月第一天是周几,month为实际月份，一月即为1,返回0即为周日
            return new Date(year,month-1,0).getDay();
        },
        createMon : function(){
            var t= this,html='';
            var m = t.nt.getMonth()+1;
            m = m == 0 ? 12 : m;
            for(var i = 1;i<=12;i++){
                html+='<div class="calender-mon-cell '+( m == i ? 'active' : '') +' ">'+ (i) +'</div>';
            };
            g('.calender-list3').innerHTML = html;
            var cells = doc.querySelectorAll('.calender-mon-cell');
            for(var i2 = 0;i2<cells.length;i2++){
                cells[i2].onclick = function(){
                    t.moff = false
                    t.del(g('.calender-wrap'),'month');
                    t.nt.setDate(1)
                    t.nt.setMonth(+this.innerHTML-1);
                    t.createDay();
                }
            }
        },
        createYear : function(){
            var t= this,html='',y = (t.nt.getFullYear());
            var Year = g('#calender-year');
            for(var i = 0;i<9;i++){
                html+='<div class="calender-year-cell '+( (y-(4-i)) == y ? 'active' :'') +' ">'+ (y-(4-i)) +'</div>';
            }
            Year.innerHTML = y
            g('.calender-list2').innerHTML = html;
            var cells = doc.querySelectorAll('.calender-year-cell');
            for(var i2 = 0;i2<cells.length;i2++){
                cells[i2].onclick = function(){
                    t.yoff = false;
                    t.del(g('.calender-wrap'),'year');
                    t.nt.setFullYear(+this.innerHTML);
                    t.createDay();
                }
            }
        },
        createDay : function(n){
            var t = this, 
                y = t.nt.getFullYear(),
                m = (t.nt.getMonth())+1;
            g('#calender-year').innerHTML = m===0 ? y-1 : y;
            g('#calender-mon').innerHTML = m === 0 ? 12 : two(m);
            // if(t.nt.getMonth()+1 == t.s.date[1] && t.nt.getFullYear()==t.s.date[0] ){
            //  t.nt.setDate(t.s.date[2]);
            // };
            var firstDay = this.getFirstDay(y,m),
                length = this.getDateLength(y,m),
                lastMonthLength = this.getDateLength(y,m-1),
                i,html = '';
                t.day = t.s.date[2] > length ? length : t.s.date[2];
            //循环输出月前空格
            if(firstDay ===0) firstDay = 7;
            for(i=1;i<firstDay+1;i++){
                html += '<div class="calender-cell calender-cell-dark">' + (lastMonthLength - firstDay + i) + '</div>';
            }
            //循环输出当前月所有天
            for(i=1;i<length+1;i++){
                html += '<div data-n='+i+' class="calender-cell '+ (i == t.day ? 'active' :'') +'">' + i + '</div>';
            }
            //if(8-(length+firstDay)%7 !=8){
            for(i=1;i<= (41-(length+(firstDay==0 ? 7 : firstDay)-1));i++){
                html+= '<div class="calender-cell calender-cell-dark">' + i + '</div>';
            };
            doc.querySelector('.calender-content').innerHTML = html
        },
        create : function(){
            var t= this;
            if( g('.calender-wrap')) doc.body.removeChild( g('.calender-wrap') )
            var private_Day_title=['一','二','三','四','五','六','日'];
            //内容
            var html = '<div class="calender-wrap">';
            html +='<div id="calender-header" class="calender-header none-btn "><a id="calender-prev" href="javascript:;"><</a><a id="calender-next" href="javascript:;">></a> <span id="calender-year">2016</span>年<span id="calender-mon">10</span>月</div>'
            //星期
            html += '<div class="calender-list"><div class="calender-caption">';
            for(i=0;i<7;i++){
                html += '<div class="calender-cell">' + private_Day_title[i] + '</div>';
            };
            html += '</div><div class="calender-content"></div>';
            if(this.s.button){
                html+='<div class="calender-button"><a href="javascript:;" class="calender-ent">确定</a><a href="javascript:;" class="calender-today">今天</a></div>';
            };
            html += '</div><div class="calender-list calender-list2"></div><div class="calender-list calender-list3"></div>'
            doc.body.insertAdjacentHTML("beforeend", html);
            var wrap = g('.calender-wrap');
            function setPosi(){
                var _top = doc.documentElement.scrollTop || doc.body.scrollTop;
                wrap.style.left = t.dom.getBoundingClientRect().left +t.s.left +'px';;
                wrap.style.top = t.dom.getBoundingClientRect().top + _top + t.dom.offsetHeight+t.s.top + 15 +'px';
            };
            setPosi();
            addEvent(window,'resize',function(){setPosi()})
            wrap.onclick = function(ev){
                var e = ev || event;
                e.stopPropagation ? e.stopPropagation() : (e.cancelBubble = true)
            }
        },
     format : function(da,format){
        var _newDate = new Date(da);
            var WeekArr=['星期日','星期一','星期二','星期三','星期四','星期五','星期六']; 
         var o = { 
          'M+' : _newDate.getMonth()+1, //month 
          'd+' : _newDate.getDate(), //day 
          'h+' : _newDate.getHours(), //hour 
          'm+' : _newDate.getMinutes(), //minute 
          's+' : _newDate.getSeconds(), //second 
          'q+' : Math.floor((_newDate.getMonth()+3)/3), //quarter 
          'S': _newDate.getMilliseconds(), //millisecond 
          'E': WeekArr[_newDate.getDay()], 
          'e+' : _newDate.getDay() 
         }; 
         if (/(y+)/.test(format)){
            format = format.replace(RegExp.$1, (_newDate.getFullYear()+"").substr(4 - RegExp.$1.length));
         };
         for(var k in o) { 
          if(new RegExp('('+ k +')').test(format)) { 
           format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ('00'+ o[k]).substr((''+ o[k]).length)); 
          }; 
         }; 
         return format; 
     },
     extend : function(n,n1){
      for(var i in n1){n[i] = n1[i]};
     },
        has : function(o,n){
         return new RegExp('\\b'+n+'\\b').test(o.className); 
     },
        add : function(o,n){
         if(!this.has(o, n)) o.className+=' '+n; 
     },
        del : function(o,n){
         if(this.has(o, n)){ 
          o.className = o.className.replace(new RegExp('(?:^|\\s)'+n+'(?=\\s|$)'), '').replace(/^\s*|\s*$/g, ''); 
         }; 
     }
    };
    function g(str){return doc.querySelector(str)};
    function addEvent(obj,name,fn){obj.addEventListener? obj.addEventListener(name, fn, false):obj.attachEvent('on'+name,fn);};
 function two(num){return num<10 ? ('0'+num) : (''+num)};
    addEvent(doc,'click',function(){
        if( g('.calender-wrap')) doc.body.removeChild( g('.calender-wrap') )
    });
    function c(o){return new C(o)};return c;
})(window,document);
 
;(function(){
  calender('#calend').init(function(date){
        this.innerHTML = date
        //alert(date)
        calend=0
        water_in = []
        water_out = []
        COD = []
        BOD = []
        x_update = []
        loadDateXMLDoc(date)
        //alert('跳转到历史数据')
        //alert(COD)
        //alert(x_update)
        //alert('COD OVER')
        //alert(option_BOD)
        Chart_water_in = echarts.init(document.getElementById("Water_in"));
	    Chart_water_out = echarts.init(document.getElementById("Water_out"));
	    Chart_COD = echarts.init(document.getElementById("Water_COD"));
	    Chart_BOD = echarts.init(document.getElementById("Water_BOD"));

	    option_water_in = {
        title : {
            text: '进水流量',
        },
        tooltip : {
            trigger: 'axis'
        },

        //右上角工具条
        toolbox: {
            show : false,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : x_update
            }
        ],
        yAxis : [
            {
                type : 'value',
                axisLabel : {
                    formatter: '{value} m^3/s'
                }
            }
        ],
        series : [
            {
                name:'进水流量',
                type:'line',
				color:'red',
                data:water_in,
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name: '平均值',color:'black'}
                    ]
                }
            }

        ]
    };
	option_water_out = {
        title : {
            text: '出水流量',
        },
        tooltip : {
            trigger: 'axis'
        },

        //右上角工具条
        toolbox: {
            show : false,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : x_update
            }
        ],
        yAxis : [
            {
                type : 'value',
                axisLabel : {
                    formatter: '{value} m^3/s'
                }
            }
        ],
        series : [
            {
                name:'出水流量',
                type:'line',
                data:water_out,
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name: '平均值'}
                    ]
                }
            }

        ]
    };
	option_COD = {
        title : {
            text: 'COD',
        },
        tooltip : {
            trigger: 'axis'
        },

        //右上角工具条
        toolbox: {
            show : false,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : x_update
            }
        ],
        yAxis : [
            {
                type : 'value',
            }
        ],
        series : [
            {
                name:'COD',
                type:'line',
                data:COD,
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name: '平均值'}
                    ]
                }
            }

        ]
    };
	option_BOD = {
        title : {
            text: 'BOD',
        },
        tooltip : {
            trigger: 'axis'
        },
        //右上角工具条
        toolbox: {
            show : false,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : x_update
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : [
            {
                name:'BOD',
                type:'line',
                data:BOD,
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name: '平均值'}
                    ]
                }
            }

        ]
    };

    Chart_water_in.setOption(option_water_in);
	Chart_water_out.setOption(option_water_out);
	Chart_COD.setOption(option_COD);
	Chart_BOD.setOption(option_BOD);
	//alert('over')
    });
    // calender('#calend1').init({format : 'yyyy-MM-dd',
    // date : [2020,5,12],
    //     button : true
    // },function(date){
    //     this.innerHTML = date
    // });
})();


function loadDateXMLDoc(date)
{
	//今天的时间
	var max_length
	var mytime
	var my_t = date
	var my_year = my_t[0]+my_t[1]+my_t[2]+my_t[3]
	var my_month = my_t[5] + my_t[6]
	var my_date = my_t[8] + my_t[9]

	//alert(my_t[0]+' '+my_t[1]+' '+my_t[2]+' '+my_t[3]+' '+my_t[4]+' '+my_t[5]+' '+my_t[6]+' '+my_t[7]+' ')
	var t_seq = 'time?'+'year='+my_year+'&month='+my_month+'&day='+my_date;
	//alert('t_seq: '+t_seq)
	var xmlhttp;
	if (window.XMLHttpRequest)
	{
		//  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
		xmlhttp=new XMLHttpRequest();
	}
	else
	{
		// IE6, IE5 浏览器执行代码
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	//alert(xmlhttp.responseText)
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            //alert('12')
			receive_All = JSON.parse(xmlhttp.responseText);
			max_length = receive_All.length
			for (var i=0;i < max_length; i++){
			    water_in.push(receive_All[max_length-1-i].water_in)
			    water_out.push(receive_All[max_length-1-i].water_out)
			    COD.push(receive_All[max_length-1-i].COD)
	            BOD.push(receive_All[max_length-1-i].BOD)
	            mytime = receive_All[max_length-1-i].timestamp;
			    x_update.push(format(mytime));
			}
		}
	}
	//改一下时间
	xmlhttp.open("GET","http://127.0.0.1:8000/api/machine/controler/"+t_seq+"&format=json",false);
	xmlhttp.send();
};