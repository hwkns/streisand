
declare const process: {
    env: {
        NODE_ENV: 'development' | 'production';
    }
};

const isProd = process.env.NODE_ENV === 'production';

export default {
    apiUrl: isProd ? 'http://dev.ronzertnert.xyz:8000/api/v1' : 'http://localhost:5000/api/v1'
};