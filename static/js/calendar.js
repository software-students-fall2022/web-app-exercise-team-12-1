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


/*
[{}{}]
look up dataset attribute html
css grid
document.createElement
appendChild method

<div id="year">
    <div id="year-month">
        <div class="grid">
            *header(english days) can go either side
                <div id="year-month-day" class="calendar day">
                </div>
        </div>
    </div>
</div>
*/