export const isUndefinedOrNull = (value: any): boolean => {
    return value === undefined || value === null;
}

export const isNotUndefinedNorNull = (value: any): boolean => {
    return !isUndefinedOrNull(value);
}

export const formatNumber = (number: number | undefined | null) => {
    return number?.toFixed(2);
};