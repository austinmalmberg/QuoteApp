
function valueAttributeFor(node) {
    return 'value' in node ? 'value' : 'innerText';
}

function formatExpression(calcString) {
    const resultArray = [];

    for (const segment of calcString.split(' ')) {

        // treat segments starting with '#' as ids
        if (segment.startsWith('#')) {
            const formattedId = segment.replace('#', '', 1);
            const targetNode = document.getElementById(formattedId);
            const targetsValueAttribute = valueAttributeFor(targetNode);
            const segmentValue = targetNode[targetsValueAttribute];

            resultArray.push(segmentValue);

        // treat all else as something that can interpreted by the math library
        } else {
            resultArray.push(segment);
        }
    }

    return resultArray.join(' ');
}

function asDecimal(str, places) {
    const f = parseFloat(str);
    const modifier = places * 10;
    return ((f * modifier) / modifier).toFixed(places);
}

function htmlCalculate(node, eventName) {
    const calcString = node.getAttribute('data-calc');

    console.log('calculating', calcString)

    // replace ids with values
    const expression = formatExpression(calcString);

    // evaluate expression
    const result = math.evaluate(expression);

    // update value
    const valueAttribute = valueAttributeFor(node);

    const valueChanged = (node[valueAttribute] !== result);

    if (valueChanged) {
        // update the value
        node[valueAttribute] = asDecimal(result, 2);

        // simulate change event
        const event = new Event(eventName);
        node.dispatchEvent(event);
    }
}

function getCalculationDependents(node) {
    const dependents = [];

    const calcString = node.getAttribute('data-calc');
    if (calcString) {
        for (const segment of calcString.split(' ')) {
            if (segment.startsWith('#')) {
                const formattedId = segment.replace('#', '', 1);
                const dependent = document.getElementById(formattedId);
                if (!dependent) {
                    throw Error(`No element with id ${formattedId}`);
                }

                dependents.push(dependent);
            }
        }
    }

    return dependents;
}

const calculationMap = {
    /*
    elementId: array of dependents
    */
};

for (const node of document.querySelectorAll('[data-calc]')) {
    // add event listeners to the fields required by data-calc
    for (const dependent of getCalculationDependents(node)) {
        const eventName = dependent.tagName === 'INPUT' ? 'input' : 'change';
        dependent.addEventListener(eventName, () => htmlCalculate(node, eventName));
    }
}
