export class BaseApi {
  protected baseUrl: string = '';

  constructor(params: {
    baseUrl?: string;
  }) {
    if (params.baseUrl) {
      this.baseUrl = params.baseUrl.endsWith('/') 
        ? params.baseUrl.slice(0, -1)  
        : params.baseUrl;
    }
  }
}

