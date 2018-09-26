/* Count Up */

var options = {  
    useEasing: true,
      useGrouping: true,
      separator: ',',
      decimal: '.',
};
var membersCount = new CountUp('membersCount', 30000, 124, 0, 2, options);
if (!membersCount.error) {
    membersCount.start();
} else {  
    console.error(membersCount.error);
}
var supervisorsCount = new CountUp('supervisorsCount', 30000, 38, 0, 2, options);
if (!supervisorsCount.error) {
    supervisorsCount.start();
} else {  
    console.error(supervisorsCount.error);
}