
export interface IRequestOptions {
    url: string;
    method: string;
    headers?: { [name: string]: string }
    data?: any;
}

export default class Requestor {
    public static makeRequest<T>(options: IRequestOptions): Promise<T> {
        let xmlHttp = new XMLHttpRequest();
        let promise = new Promise<T>((resolve) => {
            xmlHttp.onreadystatechange = () => {
                if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
                    let result: T;
                    if (typeof xmlHttp.responseText === 'string') {
                        try {
                            result = JSON.parse(xmlHttp.responseText);
                        } catch (error) {
                            console.error(error);
                        }
                    }
                    resolve(result);
                }
            };
        });

        xmlHttp.open(options.method, options.url, true);

        if (options.headers) {
            for (const header in options.headers) {
                xmlHttp.setRequestHeader(header, options.headers[header]);
            }
        }
        xmlHttp.send(options.data || null);
        return promise;
    }
}
