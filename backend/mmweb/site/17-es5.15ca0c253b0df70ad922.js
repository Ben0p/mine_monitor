function _defineProperties(e,t){for(var n=0;n<t.length;n++){var a=t[n];a.enumerable=a.enumerable||!1,a.configurable=!0,"value"in a&&(a.writable=!0),Object.defineProperty(e,a.key,a)}}function _createClass(e,t,n){return t&&_defineProperties(e.prototype,t),n&&_defineProperties(e,n),e}function _classCallCheck(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(window.webpackJsonp=window.webpackJsonp||[]).push([[17],{p5L5:function(e,t,n){"use strict";n.r(t);var a,r=n("ofXK"),i=n("aceb"),o=n("h+2I"),c=n("tyNb"),s=n("fXoL"),l=((a=function e(){_classCallCheck(this,e)}).\u0275fac=function(e){return new(e||a)},a.\u0275cmp=s["\u0275\u0275defineComponent"]({type:a,selectors:[["ngx-wind"]],decls:1,vars:0,template:function(e,t){1&e&&s["\u0275\u0275element"](0,"router-outlet")},directives:[c.h],encapsulation:2}),a),d=n("Ikiw"),h=n("R0Ic"),u=n("9x60");function g(e,t){if(1&e&&s["\u0275\u0275element"](0,"ngx-wind-speed-card",4),2&e){var n=s["\u0275\u0275nextContext"]().$implicit;s["\u0275\u0275propertyInterpolate1"]("routerLink","/pages/wind/",n.module_uid.$oid,""),s["\u0275\u0275property"]("location",n.name)("speed",n.speed)("info",n.kmh)("status",n.status)("on",n.online)}}function m(e,t){if(1&e&&(s["\u0275\u0275elementStart"](0,"div",2),s["\u0275\u0275template"](1,g,1,6,"ngx-wind-speed-card",3),s["\u0275\u0275elementEnd"]()),2&e){var n=t.$implicit;s["\u0275\u0275advance"](1),s["\u0275\u0275property"]("ngIf","speed"==n.type)}}var b,p,f,C,y=((b=function(){function e(t){_classCallCheck(this,e),this.wind=t,this.direction="N"}return _createClass(e,[{key:"ngOnInit",value:function(){var e=this;this.refreshData(),this.interval=setInterval((function(){e.refreshData()}),1e4)}},{key:"ngOnDestroy",value:function(){clearInterval(this.interval)}},{key:"refreshData",value:function(){var e=this;this.wind.getWindAll().subscribe((function(t){e.winds=t}))}}]),e}()).\u0275fac=function(e){return new(e||b)(s["\u0275\u0275directiveInject"](d.a))},b.\u0275cmp=s["\u0275\u0275defineComponent"]({type:b,selectors:[["all"]],decls:2,vars:1,consts:[[1,"row"],["class","col-xl-3 col-lg-4 col-md-6 col-sm-12",4,"ngFor","ngForOf"],[1,"col-xl-3","col-lg-4","col-md-6","col-sm-12"],["style","cursor: pointer;",3,"location","speed","info","status","on","routerLink",4,"ngIf"],[2,"cursor","pointer",3,"location","speed","info","status","on","routerLink"]],template:function(e,t){1&e&&(s["\u0275\u0275elementStart"](0,"div",0),s["\u0275\u0275template"](1,m,2,1,"div",1),s["\u0275\u0275elementEnd"]()),2&e&&(s["\u0275\u0275advance"](1),s["\u0275\u0275property"]("ngForOf",t.winds))},directives:[r.l,r.m,u.a,c.d],styles:[".direction[_ngcontent-%COMP%]{width:20px;height:auto}.nb-theme-default   [_nghost-%COMP%]   ngx-wind-line-chart[_ngcontent-%COMP%]{display:block;height:28.875rem;width:100%}.nb-theme-default   [_nghost-%COMP%]   ngx-wind-line-chart[_ngcontent-%COMP%]     chart{display:block;height:100%;width:100%}.nb-theme-dark   [_nghost-%COMP%]   ngx-wind-line-chart[_ngcontent-%COMP%]{display:block;height:28.875rem;width:100%}.nb-theme-dark   [_nghost-%COMP%]   ngx-wind-line-chart[_ngcontent-%COMP%]     chart{display:block;height:100%;width:100%}.nb-theme-cosmic   [_nghost-%COMP%]   ngx-wind-line-chart[_ngcontent-%COMP%]{display:block;height:28.875rem;width:100%}.nb-theme-cosmic   [_nghost-%COMP%]   ngx-wind-line-chart[_ngcontent-%COMP%]     chart{display:block;height:100%;width:100%}.nb-theme-corporate   [_nghost-%COMP%]   ngx-wind-line-chart[_ngcontent-%COMP%]{display:block;height:28.875rem;width:100%}.nb-theme-corporate   [_nghost-%COMP%]   ngx-wind-line-chart[_ngcontent-%COMP%]     chart{display:block;height:100%;width:100%}"],data:{animation:[Object(h.j)("rotatedState",[Object(h.g)("N",Object(h.h)({transform:"rotate(0)"})),Object(h.g)("NNE",Object(h.h)({transform:"rotate(22.5deg)"})),Object(h.g)("NE",Object(h.h)({transform:"rotate(45deg)"})),Object(h.g)("ENE",Object(h.h)({transform:"rotate(67.50deg)"})),Object(h.g)("E",Object(h.h)({transform:"rotate(90deg)"})),Object(h.g)("ESE",Object(h.h)({transform:"rotate(112.5deg)"})),Object(h.g)("SE",Object(h.h)({transform:"rotate(135deg)"})),Object(h.g)("SSE",Object(h.h)({transform:"rotate(157.5deg)"})),Object(h.g)("S",Object(h.h)({transform:"rotate(180deg)"})),Object(h.g)("SSW",Object(h.h)({transform:"rotate(202.5deg)"})),Object(h.g)("SW",Object(h.h)({transform:"rotate(225deg)"})),Object(h.g)("WSW",Object(h.h)({transform:"rotate(247.5deg)"})),Object(h.g)("W",Object(h.h)({transform:"rotate(270deg)"})),Object(h.g)("WNW",Object(h.h)({transform:"rotate(292.5deg)"})),Object(h.g)("NW",Object(h.h)({transform:"rotate(315deg)"})),Object(h.g)("NNW",Object(h.h)({transform:"rotate(337.5deg)"}))])]}}),b),O=n("z+eI"),v=((p=function(){function e(t,n){var a=this;_classCallCheck(this,e),this.theme=t,this.wind=n,this.unit="kmh",this.themeSubscription=this.theme.getJsTheme().subscribe((function(e){a.colors=e.variables;var t=e.variables.chartjs;a.data={labels:[],datasets:[{data:[],label:a.range,backgroundColor:i.u.hexToRgbA(a.colors.primary,.3),borderColor:a.colors.primary}]},a.options={responsive:!0,maintainAspectRatio:!1,animation:{duration:0},scales:{xAxes:[{gridLines:{display:!0,color:t.axisLineColor},ticks:{fontColor:t.textColor}}],yAxes:[{gridLines:{display:!0,color:t.axisLineColor},ticks:{fontColor:t.textColor}}]},legend:{labels:{fontColor:t.textColor}}}}))}return _createClass(e,[{key:"refreshData",value:function(){var e=this;"minute"==this.range?this.wind.getWindMinute(this.uid).subscribe((function(t){e.name=t.name,e.windspeed=t,e.loadData(e.windspeed)})):"hour"==this.range?this.wind.getWindHour(this.uid).subscribe((function(t){e.name=t.name,e.windspeed=t,e.loadData(e.windspeed)})):"day"==this.range?this.wind.getWindDay(this.uid).subscribe((function(t){e.name=t.name,e.windspeed=t,console.log(t),e.loadData(e.windspeed)})):"month"==this.range&&this.wind.getWindMonth(this.uid).subscribe((function(t){e.name=t.name,e.windspeed=t,console.log(t),e.loadData(e.windspeed)}))}},{key:"ngOnInit",value:function(){var e=this;this.refreshData(),this.interval=setInterval((function(){e.refreshData()}),1e4)}},{key:"ngOnDestroy",value:function(){this.themeSubscription.unsubscribe(),clearInterval(this.interval)}},{key:"loadData",value:function(e){this.data="minute"==this.range?{labels:e.time,datasets:[{data:e[this.unit].speed,label:"Speed",backgroundColor:i.u.hexToRgbA(this.colors.primary,.3),borderColor:this.colors.primary}]}:{labels:e.time,datasets:[{data:e[this.unit].max,label:"max",backgroundColor:i.u.hexToRgbA(this.colors.danger,.3),borderColor:this.colors.danger},{data:e[this.unit].min,label:"min",backgroundColor:i.u.hexToRgbA(this.colors.success,.3),borderColor:this.colors.success},{data:e[this.unit].avg,label:"avg",backgroundColor:i.u.hexToRgbA(this.colors.primary,.3),borderColor:this.colors.primary}]}}}]),e}()).\u0275fac=function(e){return new(e||p)(s["\u0275\u0275directiveInject"](i.mb),s["\u0275\u0275directiveInject"](d.a))},p.\u0275cmp=s["\u0275\u0275defineComponent"]({type:p,selectors:[["ngx-wind-line-chart"]],inputs:{uid:"uid",range:"range"},decls:12,vars:8,consts:[[3,"value","valueChange","click"],[3,"value","click"],["type","line",3,"data","options"]],template:function(e,t){1&e&&(s["\u0275\u0275elementStart"](0,"nb-card"),s["\u0275\u0275elementStart"](1,"nb-card-header"),s["\u0275\u0275text"](2),s["\u0275\u0275elementStart"](3,"nb-radio-group",0),s["\u0275\u0275listener"]("valueChange",(function(e){return t.unit=e}))("click",(function(){return t.refreshData()})),s["\u0275\u0275elementStart"](4,"nb-radio",1),s["\u0275\u0275listener"]("click",(function(){return t.refreshData()})),s["\u0275\u0275text"](5," km/h "),s["\u0275\u0275elementEnd"](),s["\u0275\u0275elementStart"](6,"nb-radio",1),s["\u0275\u0275listener"]("click",(function(){return t.refreshData()})),s["\u0275\u0275text"](7," m/s "),s["\u0275\u0275elementEnd"](),s["\u0275\u0275elementStart"](8,"nb-radio",1),s["\u0275\u0275listener"]("click",(function(){return t.refreshData()})),s["\u0275\u0275text"](9," knots "),s["\u0275\u0275elementEnd"](),s["\u0275\u0275elementEnd"](),s["\u0275\u0275elementEnd"](),s["\u0275\u0275elementStart"](10,"nb-card-body"),s["\u0275\u0275element"](11,"chart",2),s["\u0275\u0275elementEnd"](),s["\u0275\u0275elementEnd"]()),2&e&&(s["\u0275\u0275advance"](2),s["\u0275\u0275textInterpolate2"](" ",t.name," - ",t.range," "),s["\u0275\u0275advance"](1),s["\u0275\u0275property"]("value",t.unit),s["\u0275\u0275advance"](1),s["\u0275\u0275property"]("value","kmh"),s["\u0275\u0275advance"](2),s["\u0275\u0275property"]("value","ms"),s["\u0275\u0275advance"](2),s["\u0275\u0275property"]("value","knots"),s["\u0275\u0275advance"](3),s["\u0275\u0275property"]("data",t.data)("options",t.options))},directives:[i.n,i.p,i.Z,i.Y,i.m,O.ChartComponent],styles:[".nb-theme-default   [_nghost-%COMP%]   nb-card-body[_ngcontent-%COMP%]{display:block;height:28.875rem;width:100%}.nb-theme-default   [_nghost-%COMP%]   nb-card-body[_ngcontent-%COMP%]     chart{display:block;height:100%;width:100%}.nb-theme-dark   [_nghost-%COMP%]   nb-card-body[_ngcontent-%COMP%]{display:block;height:28.875rem;width:100%}.nb-theme-dark   [_nghost-%COMP%]   nb-card-body[_ngcontent-%COMP%]     chart{display:block;height:100%;width:100%}.nb-theme-cosmic   [_nghost-%COMP%]   nb-card-body[_ngcontent-%COMP%]{display:block;height:28.875rem;width:100%}.nb-theme-cosmic   [_nghost-%COMP%]   nb-card-body[_ngcontent-%COMP%]     chart{display:block;height:100%;width:100%}.nb-theme-corporate   [_nghost-%COMP%]   nb-card-body[_ngcontent-%COMP%]{display:block;height:28.875rem;width:100%}.nb-theme-corporate   [_nghost-%COMP%]   nb-card-body[_ngcontent-%COMP%]     chart{display:block;height:100%;width:100%}nb-radio-group[_ngcontent-%COMP%]{display:table}nb-radio[_ngcontent-%COMP%]{display:table-cell}"]}),p),w=[{path:"",component:l,children:[{path:"all",component:y},{path:":uid",component:(f=function(){function e(t){_classCallCheck(this,e),this.route=t}return _createClass(e,[{key:"ngOnInit",value:function(){this.uid=this.route.snapshot.paramMap.get("uid")}}]),e}(),f.\u0275fac=function(e){return new(e||f)(s["\u0275\u0275directiveInject"](c.a))},f.\u0275cmp=s["\u0275\u0275defineComponent"]({type:f,selectors:[["detail"]],decls:9,vars:8,consts:[[1,"row"],[1,"col-12"],[3,"uid","range"]],template:function(e,t){1&e&&(s["\u0275\u0275elementStart"](0,"div",0),s["\u0275\u0275elementStart"](1,"div",1),s["\u0275\u0275element"](2,"ngx-wind-line-chart",2),s["\u0275\u0275elementEnd"](),s["\u0275\u0275elementStart"](3,"div",1),s["\u0275\u0275element"](4,"ngx-wind-line-chart",2),s["\u0275\u0275elementEnd"](),s["\u0275\u0275elementStart"](5,"div",1),s["\u0275\u0275element"](6,"ngx-wind-line-chart",2),s["\u0275\u0275elementEnd"](),s["\u0275\u0275elementStart"](7,"div",1),s["\u0275\u0275element"](8,"ngx-wind-line-chart",2),s["\u0275\u0275elementEnd"](),s["\u0275\u0275elementEnd"]()),2&e&&(s["\u0275\u0275advance"](2),s["\u0275\u0275property"]("uid",t.uid)("range","minute"),s["\u0275\u0275advance"](2),s["\u0275\u0275property"]("uid",t.uid)("range","hour"),s["\u0275\u0275advance"](2),s["\u0275\u0275property"]("uid",t.uid)("range","day"),s["\u0275\u0275advance"](2),s["\u0275\u0275property"]("uid",t.uid)("range","month"))},directives:[v],styles:[""]}),f)}]}],k=((C=function e(){_classCallCheck(this,e)}).\u0275mod=s["\u0275\u0275defineNgModule"]({type:C}),C.\u0275inj=s["\u0275\u0275defineInjector"]({factory:function(e){return new(e||C)},imports:[[c.g.forChild(w)],c.g]}),C);n.d(t,"WindModule",(function(){return j}));var _,j=((_=function e(){_classCallCheck(this,e)}).\u0275mod=s["\u0275\u0275defineNgModule"]({type:_}),_.\u0275inj=s["\u0275\u0275defineInjector"]({factory:function(e){return new(e||_)},imports:[[k,r.c,o.a,i.q]]}),_)}}]);