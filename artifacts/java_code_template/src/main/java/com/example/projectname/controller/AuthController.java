package com.example.projectname.controller;

import com.example.projectname.dtos.RegisterRequest;
import com.example.projectname.dtos.LoginRequest;
import com.example.projectname.service.AuthService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

/**
 * AuthController handles user authentication operations such as registration,
 * login, and logout.
 */
@RestController
public class AuthController {

    @Autowired
    private AuthService authService;

    /**
     * Registers a new user with the provided registration details.
     *
     * @param registerRequest the registration details
     * @return a ResponseEntity indicating the result of the registration
     */
    @PostMapping("/auth/register")
    public ResponseEntity<?> register(@RequestBody RegisterRequest registerRequest) {
        try {
            authService.register(
                    registerRequest.getUsername(),
                    registerRequest.getEmail(),
                    registerRequest.getPassword(),
                    registerRequest.getRole());
            return ResponseEntity.status(201).build();
        } catch (Exception e) {
            throw e;
            // return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    /**
     * Authenticates a user and returns a JWT token.
     *
     * @param loginRequest the login credentials
     * @return a ResponseEntity containing the JWT token if authentication is
     *         successful
     */
    @PostMapping("/auth/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest loginRequest) {
        try {
            String token = authService.login(loginRequest.getEmail(), loginRequest.getPassword());
            return ResponseEntity.ok(token);
        } catch (Exception e) {
            return ResponseEntity.status(401).body(e.getMessage());
        }
    }

    /**
     * Logs out the authenticated user by invalidating the JWT token.
     *
     * @param authorizationHeader the Authorization header containing the JWT token
     * @return a ResponseEntity indicating the result of the logout
     */
    @PostMapping("/auth/logout")
    public ResponseEntity<?> logout(@RequestHeader("Authorization") String authorizationHeader) {
        try {
            // Extract the token from the Authorization header
            String token = authorizationHeader.replace("Bearer ", "");
            authService.logout(token);
            return ResponseEntity.ok().build();
        } catch (Exception e) {
            return ResponseEntity.status(401).body(e.getMessage());
        }
    }
}