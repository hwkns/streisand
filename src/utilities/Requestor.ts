
export interface IRequestOptions {
    url: string;
    method: string;
    headers?: { [name: string]: string };
    data?: any;
}

function parseResponse<T>(request: XMLHttpRequest): T {
    let result: T;
    if (request.responseText && typeof request.responseText === 'string') {
        try {
            result = JSON.parse(request.responseText);
        } catch (error) {
            console.error(error);
        }
    }
    return result;
}

export default class Requestor {
    public static makeRequest<T>(options: IRequestOptions): Promise<T> {
        let xmlHttp = new XMLHttpRequest();
        let promise = new Promise<T>((resolve, reject) => {
            xmlHttp.onreadystatechange = () => {
                if (xmlHttp.readyState === 4) {
                    const result = parseResponse<T>(xmlHttp);
                    if (xmlHttp.status >= 200 && xmlHttp.status < 300) {
                        resolve(result);
                    } else if (xmlHttp.status >= 400) {
                        reject({
                            status: xmlHttp.status,
                            result: result
                        });
                    }
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
