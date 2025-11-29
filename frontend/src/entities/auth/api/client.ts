import axios from "axios";
import { LoginDto, LoginResponseDto } from "../types";
import { BaseApi } from "@/shared/api/base-api";
import { SignUpDto, SignUpResponseDto } from "../types/signup-dto";

export class AuthApi extends BaseApi {
  async login(params: LoginDto): Promise<LoginResponseDto> {
    try {
      const res = await axios.post(`${this.baseUrl}/auth/login`, params);
      return res.data;
    } catch (err) {
      throw err;
    }
  }

  async signUp(params: SignUpDto): Promise<SignUpResponseDto> {
    try {
      const res = await axios.post(`${this.baseUrl}/auth/signup`, params);
      return res.data;
    } catch (err) {
      throw err;
    }
  }

  async isAuthenticated(): Promise<boolean> {
    try {
      const res = await axios.get(`${this.baseUrl}/auth/is-authenticated`);
      return res.data.success;
    } catch (err) {
      throw err;
   }
  }
}

export const authClient = new AuthApi({
  baseUrl: '/api/proxy/main-api'
});
