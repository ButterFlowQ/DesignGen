package com.example.projectname.security;

import com.example.projectname.enums.UserRole;
import io.jsonwebtoken.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.Date;
import java.util.UUID;

@Component
public class JwtTokenProvider {

    @Value("${app.jwt-secret}")
    private String jwtSecret;

    @Value("${app.jwt-expiration-in-ms}")
    private long jwtExpirationInMs;

    /**
     * Creates a JWT token with user-specific claims:
     * - UUID as userId
     * - Enum as userRole
     * - tokenVersion (int)
     */
    public String createToken(UUID userId, UserRole userRole, int tokenVersion) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + jwtExpirationInMs);

        return Jwts.builder()
                // Store userId in the subject (optional but convenient).
                .setSubject(userId.toString())
                .setIssuedAt(now)
                .setExpiration(expiryDate)

                // Custom claims
                .claim("userId", userId.toString())          // Store UUID as a string
                .claim("role", userRole.name())              // Store enum as its name()
                .claim("tokenVersion", tokenVersion)

                // Sign with your secret key
                .signWith(SignatureAlgorithm.HS512, jwtSecret)
                .compact();
    }

    /**
     * Validates the JWT token.
     *
     * @param token the JWT token
     * @return true if the token is valid; false otherwise
     */
    public boolean validateToken(String token) {
        try {
            Jwts.parser()
                    .setSigningKey(jwtSecret)
                    .parseClaimsJws(token); // Will throw if invalid or expired
            return true;
        } catch (SignatureException ex) {
            System.out.println("Invalid JWT signature: " + ex.getMessage());
        } catch (MalformedJwtException ex) {
            System.out.println("Invalid JWT token: " + ex.getMessage());
        } catch (ExpiredJwtException ex) {
            System.out.println("Expired JWT token: " + ex.getMessage());
        } catch (UnsupportedJwtException ex) {
            System.out.println("Unsupported JWT token: " + ex.getMessage());
        } catch (IllegalArgumentException ex) {
            System.out.println("JWT claims string is empty: " + ex.getMessage());
        }
        return false;
    }

    /**
     * Extract all Claims from the token.
     */
    private Claims getAllClaimsFromToken(String token) {
        return Jwts.parser()
                .setSigningKey(jwtSecret)
                .parseClaimsJws(token)
                .getBody();
    }

    /**
     * Get userId (UUID) from the token.
     */
    public UUID getUserIdFromToken(String token) {
        Claims claims = getAllClaimsFromToken(token);
        String userIdString = claims.get("userId", String.class);
        return UUID.fromString(userIdString);
    }

    /**
     * Get userRole (enum) from the token.
     */
    public UserRole getRoleFromToken(String token) {
        Claims claims = getAllClaimsFromToken(token);
        String roleString = claims.get("role", String.class);
        return UserRole.valueOf(roleString);
    }

    /**
     * Get tokenVersion (int) from the token.
     */
    public int getTokenVersionFromToken(String token) {
        Claims claims = getAllClaimsFromToken(token);
        Integer version = claims.get("tokenVersion", Integer.class);
        return (version != null) ? version : 0;
    }
}

