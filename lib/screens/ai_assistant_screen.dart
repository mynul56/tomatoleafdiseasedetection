import 'package:flutter/material.dart';
import '../models/chat_message.dart';
import '../services/groq_service.dart';
import '../services/voice_service.dart';

class AiAssistantScreen extends StatefulWidget {
  const AiAssistantScreen({super.key});

  @override
  State<AiAssistantScreen> createState() => _AiAssistantScreenState();
}

class _AiAssistantScreenState extends State<AiAssistantScreen> {
  final List<ChatMessage> _messages = [];
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final GroqService _groqService = GroqService();
  final VoiceService _voiceService = VoiceService();

  bool _isLoading = false;
  bool _isListening = false;
  bool _isSpeaking = false;
  bool _voiceInitialized = false;

  @override
  void initState() {
    super.initState();
    _initializeVoice();
    _addWelcomeMessage();
  }

  Future<void> _initializeVoice() async {
    _voiceInitialized = await _voiceService.initialize();
    if (!_voiceInitialized) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Microphone permission required for voice assistant'),
          ),
        );
      }
    }
  }

  void _addWelcomeMessage() {
    setState(() {
      _messages.add(
        ChatMessage(
          text:
              '👋 Hello! I\'m your AI assistant for tomato plant care.\n\n🧪 Currently running in DEMO MODE with sample responses.\n\nAsk me about tomato leaf diseases, treatments, or plant care!\n\n💡 To get full AI responses, add your Groq API key in lib/config/api_config.dart',
          isUser: false,
        ),
      );
    });
  }

  Future<void> _sendMessage(String text) async {
    if (text.trim().isEmpty) return;

    setState(() {
      _messages.add(ChatMessage(text: text, isUser: true));
      _isLoading = true;
    });

    _textController.clear();
    _scrollToBottom();

    try {
      final response = await _groqService.sendMessage(text);

      setState(() {
        _messages.add(ChatMessage(text: response, isUser: false));
        _isLoading = false;
      });

      _scrollToBottom();
    } catch (e) {
      setState(() {
        _messages.add(
          ChatMessage(
            text: e.toString().replaceAll('Exception: ', ''),
            isUser: false,
          ),
        );
        _isLoading = false;
      });
    }
  }

  Future<void> _startListening() async {
    if (!_voiceInitialized) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'Voice service not available. Grant microphone permission in Settings.',
          ),
        ),
      );
      return;
    }

    setState(() {
      _isListening = true;
    });

    // Show feedback to user
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('🎤 Listening... Speak now!'),
          duration: Duration(seconds: 2),
        ),
      );
    }

    try {
      final recognizedText = await _voiceService.listen();

      setState(() {
        _isListening = false;
      });

      if (recognizedText.isNotEmpty) {
        await _sendMessage(recognizedText);
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('No speech detected. Please try again.'),
              duration: Duration(seconds: 2),
            ),
          );
        }
      }
    } catch (e) {
      setState(() {
        _isListening = false;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Voice error: ${e.toString().replaceAll('Exception: ', '')}',
            ),
            duration: const Duration(seconds: 3),
          ),
        );
      }
    }
  }

  Future<void> _speakMessage(String text) async {
    if (!_voiceInitialized) return;

    setState(() {
      _isSpeaking = true;
    });

    await _voiceService.speak(text);

    // Wait for speech to complete
    await Future.delayed(Duration(milliseconds: text.length * 50));

    if (mounted) {
      setState(() {
        _isSpeaking = false;
      });
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    _voiceService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Assistant'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Column(
        children: [
          // Quick action buttons
          Container(
            padding: const EdgeInsets.all(8),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  _buildQuickActionChip(
                    'Common Diseases',
                    () => _sendMessage(
                      'What are the most common tomato leaf diseases?',
                    ),
                  ),
                  const SizedBox(width: 8),
                  _buildQuickActionChip(
                    'Prevention Tips',
                    () => _sendMessage(
                      'How can I prevent tomato plant diseases?',
                    ),
                  ),
                  const SizedBox(width: 8),
                  _buildQuickActionChip(
                    'Treatment Guide',
                    () => _sendMessage(
                      'What are general treatment options for tomato diseases?',
                    ),
                  ),
                ],
              ),
            ),
          ),
          const Divider(height: 1),

          // Chat messages
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length + (_isLoading ? 1 : 0),
              itemBuilder: (context, index) {
                if (index == _messages.length) {
                  return _buildLoadingIndicator();
                }

                final message = _messages[index];
                return _buildMessageBubble(message);
              },
            ),
          ),

          const Divider(height: 1),

          // Input area
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
            child: Row(
              children: [
                // Voice button
                IconButton(
                  onPressed: _isListening ? null : _startListening,
                  icon: Icon(
                    _isListening ? Icons.mic : Icons.mic_none,
                    color: _isListening ? Colors.red : Colors.green,
                  ),
                  tooltip: 'Voice input',
                ),

                // Text input
                Expanded(
                  child: TextField(
                    controller: _textController,
                    decoration: InputDecoration(
                      hintText: _isListening
                          ? 'Listening...'
                          : 'Ask me anything...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(24),
                      ),
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 8,
                      ),
                    ),
                    onSubmitted: _sendMessage,
                    enabled: !_isLoading && !_isListening,
                  ),
                ),

                const SizedBox(width: 8),

                // Send button
                IconButton(
                  onPressed: _isLoading || _isListening
                      ? null
                      : () => _sendMessage(_textController.text),
                  icon: const Icon(Icons.send),
                  tooltip: 'Send message',
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildQuickActionChip(String label, VoidCallback onTap) {
    return ActionChip(
      label: Text(label),
      onPressed: onTap,
      avatar: const Icon(Icons.lightbulb_outline, size: 18),
    );
  }

  Widget _buildMessageBubble(ChatMessage message) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        mainAxisAlignment: message.isUser
            ? MainAxisAlignment.end
            : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!message.isUser) ...[
            CircleAvatar(
              backgroundColor: Colors.green.shade700,
              child: const Icon(Icons.smart_toy, color: Colors.white, size: 20),
            ),
            const SizedBox(width: 8),
          ],

          Flexible(
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: message.isUser
                    ? Colors.blue.shade700
                    : Colors.grey.shade200,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    message.text,
                    style: TextStyle(
                      color: message.isUser ? Colors.white : Colors.black87,
                      fontSize: 15,
                    ),
                  ),
                  if (!message.isUser) ...[
                    const SizedBox(height: 8),
                    GestureDetector(
                      onTap: () => _speakMessage(message.text),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(
                            _isSpeaking
                                ? Icons.volume_up
                                : Icons.volume_up_outlined,
                            size: 16,
                            color: Colors.grey.shade600,
                          ),
                          const SizedBox(width: 4),
                          Text(
                            'Listen',
                            style: TextStyle(
                              color: Colors.grey.shade600,
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ],
              ),
            ),
          ),

          if (message.isUser) ...[
            const SizedBox(width: 8),
            CircleAvatar(
              backgroundColor: Colors.blue.shade700,
              child: const Icon(Icons.person, color: Colors.white, size: 20),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildLoadingIndicator() {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        children: [
          CircleAvatar(
            backgroundColor: Colors.green.shade700,
            child: const Icon(Icons.smart_toy, color: Colors.white, size: 20),
          ),
          const SizedBox(width: 8),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.grey.shade200,
              borderRadius: BorderRadius.circular(16),
            ),
            child: const Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                SizedBox(
                  width: 16,
                  height: 16,
                  child: CircularProgressIndicator(strokeWidth: 2),
                ),
                SizedBox(width: 8),
                Text('Thinking...'),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
