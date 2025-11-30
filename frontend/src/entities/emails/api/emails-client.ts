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

  async getEmailGraph(emailId: string): Promise<{ message: string } | undefined> {
    try {
      const res = await axios.get(`${this.baseUrl}/email/${emailId}?type=graph`);
      return res.data;
    } catch {
      return undefined;
    }
  }

  async answerEmail(emailId: string, query: string): Promise<{ id: string; response: string; context_data: string } | undefined> {
    try {
      const res = await axios.post(`${this.baseUrl}/email/answer/${emailId}`, { query, email_id: emailId });
      return res.data;
    } catch {
      return undefined;
    }
  }
}

export const emailsClient = new EmailsApi({
  baseUrl: '/api/proxy/main-api'
});

