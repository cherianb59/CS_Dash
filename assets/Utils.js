window.Utils = Object.assign({}, window.Utils, {
    addCSSClass: function (classListStr, newClass) {
        if (classListStr === undefined || classListStr === null) {
            classListStr = '';
        }
        var classes = classListStr.split(' ');
        if (!classes.includes(newClass)) {
            classes.push(newClass);
        }
        return classes.join(' ');
    },
    removeCSSClass: function (classListStr, classToRemove) {
        if (classListStr === undefined || classListStr === null) {
            return '';
        }
        var classes = classListStr.split(' ');
        var newClasses = classes.filter(function (cls) {
            return cls !== classToRemove;
        });
        return newClasses.join(' ');
    }
});