//format data 
const eventsObj = JSON.parse(events.replace(/'/g, "\""))
//console.log(eventsObj)
//console.log(typeof eventsObj);

//get number of days in a month
function getDaysinMonth(year,month){
    return new Date(year,month,0).getDate();
}

//get the weekday(index) of the first day of a month
function getFirstDay(year,month){
    return new Date(year,month,1).getDay();
}

//static months array
const months = [
    {longname :"January", shortname : "Jan"},
    {longname :"February", shortname : "Feb"},
    {longname :"March", shortname : "Mar"},
    {longname :"April", shortname : "Apr"},
    {longname :"May", shortname : "May"},
    {longname :"June", shortname : "Jun"},
    {longname :"July", shortname : "July"},
    {longname :"August", shortname : "Aug"},
    {longname :"September", shortname : "Sep"},
    {longname :"October", shortname : "Oct"},
    {longname :"November", shortname : "Nov"},
    {longname :"December", shortname : "Dec"}
]

const currentDate = new Date();
const currentMonth = currentDate.getMonth();
const currentYear = currentDate.getFullYear();
const yearsArray = [currentYear,currentYear+1];

function renderDays(year,month,numDays){
    const days = [];
    for (let i=1;i<=numDays;i++){
        days.push({date:`${year}-${month}-${i}`,events:[]});
    }
    return days;
}

function renderMonths(year){
    return months.map((month,index) =>{
         const numDays = getDaysinMonth(year,index+1);
         const firstDay = getFirstDay(year,index);
         const everyDay = renderDays(year,index+1,numDays);
         return {numDays:numDays,firstDay:firstDay,wholeMonth:everyDay};
    });
}

const calendarData = yearsArray.map(year =>{
    return {year,months:renderMonths(year)}
});

let calendarState = {
    selectedYear:currentYear,
    selectedMonth:currentMonth
};

function updateCalendarState(newState){
    calendarState = {...calendarState,...newState}
}

const calendarYearEl = document.getElementById("calendarYear");
const calendarMonthEl = document.getElementById("calendarMonth");
console.log(calendarYearEl.children);
calendarYearEl.children[0].textContent = calendarData[0].year;
calendarYearEl.children[1].textContent = calendarData[1].year;
calendarYearEl.children[0].value = calendarData[0].year;
calendarYearEl.children[1].value = calendarData[1].year;
const monthEls = Array.from(calendarMonthEl.children);

monthEls.forEach((month,i)=>{
    if (i === currentMonth){
        month.setAttribute("selected","selected");
    }
    month.textContent = months[i].shortname;
});

const calendarContainerEl = document.getElementById("calendar");
const weekDayEls = Array.from(calendarContainerEl.children);

function renderCalendar(){
    const selectedYearObj = calendarData.find((obj)=>obj.year===calendarState.selectedYear)
    const selectedMonthObj = selectedYearObj.months[calendarState.selectedMonth];
    console.log("month",selectedMonthObj);
    calendarContainerEl.innerHTML = "";
    weekDayEls.forEach((weekday)=>{
        calendarContainerEl.appendChild(weekday);
    });
    const calendarDaysArray = [];
    const emptyDaysArray = Array(selectedMonthObj.firstDay).fill("emptyday");
    const totalDaysArray = [...emptyDaysArray,...selectedMonthObj.wholeMonth];
    totalDaysArray.forEach((day,i)=> {
        const dayEl = document.createElement("div");
        dayEl.classList.add("day");
        function getEvents(){
        return eventsObj.filter((event)=> event.date===day.date).map((event)=>{
            return `
            <div class = "dayEvent">
            <p>${event.name}</p>
            <p>${event.time}</p>
            </div>
            `
        });
        }
        if(day==="emptyday"){
            dayEl.classList.add("emptyday");
        }
        else{
            dayEl.innerHTML = `
            <div>
                <div>
                <p>${i+1-selectedMonthObj.firstDay}</p>
                </div>
                ${getEvents().join("")}
            </div>`;
        }
        calendarContainerEl.appendChild(dayEl);
    });
}

//update year
calendarYearEl.onchange = function(event){
    updateCalendarState({selectedYear:parseInt(event.target.value)})
    renderCalendar();
}

//update month
calendarMonthEl.onchange = function(event){
    updateCalendarState({selectedMonth:parseInt(event.target.value)})
    renderCalendar();
}

renderCalendar();



