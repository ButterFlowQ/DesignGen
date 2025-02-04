package com.example.projectname.dtos;

/**
 * DTO for authentication response containing JWT token.
 */
public class AuthResponse {

    private String token;

    /**
     * Gets the JWT token.
     *
     * @return the JWT token
     */
    public String getToken() {
        return token;
    }

    /**
     * Sets the JWT token.
     *
     * @param token the JWT token to set
     */
    public void setToken(String token) {
        this.token = token;
    }
}