package com.example.projectname.controller;

import com.example.projectname.dtos.PlaceOrderRequest;
import com.example.projectname.dtos.UpdateStatusRequest;
import com.example.projectname.entities.Order;
import com.example.projectname.entities.User;
import com.example.projectname.service.OrderService;
import com.example.projectname.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

/**
 * Controller managing order-related operations such as placing orders,
 * retrieving orders, and updating order status.
 */
@RestController
@RequestMapping("/orders")
public class OrderController {

    @Autowired
    private OrderService orderService;

    @Autowired
    private UserService userService;

    /**
     * Places a new order by a customer for multiple items from a specific
     * shopkeeper.
     *
     * @param placeOrderRequest the order details
     * @return a ResponseEntity containing the placed order
     */
    @PostMapping
    public ResponseEntity<Order> placeOrder(@RequestBody PlaceOrderRequest placeOrderRequest) {
        try {
            // 1) Retrieve Authentication
            Authentication authentication = SecurityContextHolder.getContext().getAuthentication();

            // 2) Extract your custom principal
            if (authentication == null || !authentication.isAuthenticated()) {
                throw new RuntimeException("No authenticated user found.");
            }

            // If you stored your user ID in a CustomUserDetails object:
            User currentUser = userService.findByUserName(((UserDetails) authentication.getPrincipal()).getUsername());
            UUID customerId = currentUser.getId();
            Order order = orderService.placeOrder(
                    customerId,
                    placeOrderRequest.getShopkeeperId(),
                    placeOrderRequest.getItems());
            return ResponseEntity.status(201).body(order);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(null);
        }
    }

    /**
     * Retrieves a list of orders for the authenticated user, filtered by role.
     *
     * @return a ResponseEntity containing the list of orders
     */
    @GetMapping
    public ResponseEntity<List<Order>> getOrders() {
        try {
            // 1) Retrieve Authentication
            Authentication authentication = SecurityContextHolder.getContext().getAuthentication();

            // 2) Extract your custom principal
            if (authentication == null || !authentication.isAuthenticated()) {
                throw new RuntimeException("No authenticated user found.");
            }

            // If you stored your user ID in a CustomUserDetails object:
            User currentUser = userService.findByUserName(((UserDetails) authentication.getPrincipal()).getUsername());
            List<Order> orders = orderService.getOrdersForUser(currentUser.getId(), currentUser.getRole());
            return ResponseEntity.ok(orders);
        } catch (Exception e) {
            return ResponseEntity.status(401).body(null);
        }
    }

    /**
     * Retrieves detailed information for a specific order.
     *
     * @param orderId the ID of the order
     * @return a ResponseEntity containing the order details
     */
    @GetMapping("/{orderId}")
    public ResponseEntity<Order> getOrderDetails(@PathVariable UUID orderId) {
        try {
            Order order = orderService.getOrderDetails(orderId);
            return ResponseEntity.ok(order);
        } catch (Exception e) {
            return ResponseEntity.status(404).body(null);
        }
    }

    /**
     * Updates the status of a specific order.
     *
     * @param orderId             the ID of the order
     * @param updateStatusRequest the status update details
     * @return a ResponseEntity containing the updated order
     */
    @PutMapping("/{orderId}/status")
    public ResponseEntity<Order> updateOrderStatus(@PathVariable UUID orderId,
            @RequestBody UpdateStatusRequest updateStatusRequest) {
        try {
            Order order = orderService.updateOrderStatus(orderId, updateStatusRequest.getStatus());
            return ResponseEntity.ok(order);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(null);
        }
    }
}