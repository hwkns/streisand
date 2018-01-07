declare const process: {
    env: {
        NODE_ENV: 'development' | 'production';
    }
};

const isProd = process.env.NODE_ENV === 'production';

export default {
    pageSize: 50,
    apiUrl: isProd ? 'https://dev.ronzertnert.me/api/v1' : 'http://localhost:5000/api/v1'
};