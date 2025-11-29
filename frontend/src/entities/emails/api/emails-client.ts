import axios from "axios";
import { BaseApi } from "@/shared/api/base-api";

export class EmailsApi extends BaseApi {
  async submitEmailsToGroup(form: FormData): Promise<unknown> {
    try {
      const res = await axios.post(`${this.baseUrl}/email`, form);
      return res.data;
    } catch {
      return undefined;
    }
  }
}

export const emailsClient = new EmailsApi({
  baseUrl: 'api/proxy/main-api'
});

