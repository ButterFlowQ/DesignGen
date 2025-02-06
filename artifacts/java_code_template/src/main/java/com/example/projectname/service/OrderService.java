package com.example.projectname.service;

import com.example.projectname.entities.Order;
import com.example.projectname.entities.OrderItem;
import com.example.projectname.entities.InventoryItem;
import com.example.projectname.entities.User;
import com.example.projectname.repository.OrderRepository;
import com.example.projectname.repository.OrderItemRepository;
import com.example.projectname.repository.InventoryItemRepository;
import com.example.projectname.dtos.OrderItemRequest;
import com.example.projectname.enums.OrderStatus;
import com.example.projectname.enums.UserRole;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

/**
 * Service handling business logic related to orders, including placing orders,
 * retrieving orders, and updating order
 * statuses.
 */
@Service
public class OrderService {

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private OrderItemRepository orderItemRepository;

    @Autowired
    private InventoryItemRepository inventoryItemRepository;

    /**
     * Places a new order by a customer for multiple items from a specific
     * shopkeeper.
     *
     * @param customerId   the ID of the customer placing the order
     * @param shopkeeperId the ID of the shopkeeper
     * @param items        the list of items to be ordered
     * @return the placed order
     */
    public Order placeOrder(UUID customerId, UUID shopkeeperId, List<OrderItemRequest> items) {
        Order order = new Order();
        order.setCustomerId(customerId);
        order.setShopkeeperId(shopkeeperId);
        long now = System.currentTimeMillis();
        order.setCreatedAt(new Timestamp(now));
        order.setStatus(OrderStatus.created);

        List<OrderItem> orderItems = items.stream().map(itemRequest -> {
            InventoryItem inventoryItem = inventoryItemRepository.findById(itemRequest.getItemId())
                    .orElseThrow(() -> new IllegalArgumentException("Item not found"));
            OrderItem orderItem = new OrderItem();
            orderItem.setInventoryItem(inventoryItem);
            orderItem.setQuantity(itemRequest.getQuantity());
            orderItem.setPriceAtOrder(inventoryItem.getPrice());
            orderItem.setOrder(order);
            return orderItem;
        }).collect(Collectors.toList());

        order.setItems(orderItems);
        orderRepository.save(order);
        orderItemRepository.saveAll(orderItems);

        return order;
    }

    /**
     * Retrieves a list of orders for the authenticated user, filtered by role
     * (customer or shopkeeper).
     *
     * @param userId the ID of the user
     * @param role   the role of the user
     * @return a list of orders
     */
    public List<Order> getOrdersForUser(UUID userId, UserRole role) {
        if (role == UserRole.CUSTOMER) {
            return orderRepository.findByCustomerId(userId);
        } else if (role == UserRole.SHOPKEEPER) {
            return orderRepository.findByShopkeeperId(userId);
        } else {
            throw new IllegalArgumentException("Invalid user role");
        }
    }

    /**
     * Retrieves detailed information for a specific order, including items, prices,
     * and timestamps.
     *
     * @param orderId the ID of the order
     * @return the order details
     */
    public Order getOrderDetails(UUID orderId) {
        return orderRepository.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException("Order not found"));
    }

    /**
     * Updates the status of a specific order (e.g., created, processing, cancelled,
     * fulfilled).
     *
     * @param orderId the ID of the order
     * @param status  the new status of the order
     * @return the updated order
     */
    public Order updateOrderStatus(UUID orderId, OrderStatus status) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException("Order not found"));
        order.setStatus(status);
        return orderRepository.save(order);
    }
}