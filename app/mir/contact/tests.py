from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import ContactRequest


class ContactRequestModelTest(TestCase):

    # Create a sample contact request for testing
    @patch('mir.contact.views.ContactRequestCreateView._send_contact_info_as_email')
    # mock the sent email after message creation
    def setUp(self, mock_send_mail):
        # Create a sample contact request for testing
        self.contact_request = ContactRequest.objects.create(
            email='test@example.com',
            name='Test User',
            content='This is a test contact request content.',
        )

    def test_contact_request_creation(self):
        self.assertEqual(self.contact_request.email, 'test@example.com')
        self.assertEqual(self.contact_request.name, 'Test User')
        self.assertEqual(self.contact_request.content, 'This is a test contact request content.')
        self.assertIsNotNone(self.contact_request.date)
        self.assertEqual(str(self.contact_request), 'Test User')


class ContactRequestCreateViewTest(TestCase):

    # Sending a POST request to the view
    @patch('mir.contact.views.ContactRequestCreateView._send_contact_info_as_email')
    def test_contact_request_create_view(self, mock_send_mail):
        url = reverse('contact_us')

        response = self.client.post(url, {
            'email': 'test@example.com',
            'name': 'Test User',
            'content': 'This is a test contact request content.',
        })

        # Check if the form submission redirects to the success URL
        self.assertRedirects(response, reverse('success-url'))

        # Check if a new ContactRequest instance is created
        self.assertEqual(ContactRequest.objects.count(), 1)
        contact_request = ContactRequest.objects.first()
        self.assertEqual(contact_request.email, 'test@example.com')
        self.assertEqual(contact_request.name, 'Test User')
        self.assertEqual(contact_request.content, 'This is a test contact request content.')

        self.assertEqual(mock_send_mail.call_count, 1)

        # Check if the send_contact_info_as_email  was applied
        mock_send_mail.assert_called_once()
